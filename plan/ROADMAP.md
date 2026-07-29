# Tamil LLM — ROADMAP

## Goal
Build a Tamil-specialized LLM that beats **Sarvam-1** on published Tamil benchmarks.  
Fully free pipeline: no API keys, no paid services — local Ollama for synthetic data, HuggingFace free tier for datasets and model hosting.

---

## Target Scores (Sarvam-1 Tamil — published baseline)

| Benchmark | Sarvam-1 Tamil | Our Target |
|---|---|---|
| MMLU (Tamil) | 43.79 | **> 50** |
| ARC-Challenge (Tamil) | 57.04 | **> 62** |
| BoolQ (Tamil) | 79.51 | **> 83** |
| TriviaQA (Tamil) | 89.48 | **> 91** |
| Flores en→ta (chrF++) | 44.02 | **> 49** |
| XQUAD F1 (Tamil) | 41.89 | **> 50** |

---

## Model Choice

| Model | Params | Tamil coverage | Dev (8GB) | Train (40GB) | Status |
|---|---|---|---|---|---|
| **Llama 3.1 8B** | 8B | ✅ Common Crawl | 4-bit QLoRA | ✅ | **Primary** |
| Qwen 2.5 7B | 7B | Partial (18T tokens) | 4-bit QLoRA | ✅ | A/B experiment after Phase 1 |
| Llama 3.2 3B | 3B | ✅ | ✅ native | ✅ | **Local dev/config testing only** |
| Aya Expanse 8B | 8B | ❌ Tamil not listed | — | — | Eliminated |
| Sarvam-1 | 2B | ✅ 2T Indic | ✅ | ✅ | Competitor baseline only |

---

## Training Pipeline

```
Base Model (Llama 3.1 8B)
       │
       ▼
  Phase 1: CPT ──────── tawiki_chunked.jsonl (532K chunks, 845MB Wikipedia)
       │
       ▼
  Phase 2: Data Expansion ── CC-100 ta + IndicCorp + OSCAR ta (all free HF)
       │
       ▼
  Phase 3: Synthetic Data ── Local Ollama (no API cost) → 50K instruction pairs
       │
       ▼
  Phase 4: SFT ────────── Synthetic + IndicInstruct + IndicXNLI + IndicSentiment
       │
       ▼
  Phase 5: DPO ────────── Self-generated preference pairs (chosen/rejected)
       │
       ▼
  Phase 6: RLHF (later) ── Reward model + PPO (only if DPO plateaus)
       │
       ▼
  Phase 7: Eval ───────── lm-eval-harness vs Sarvam-1 → comparison table
       │
       ▼
  Phase 8: Publish ────── HuggingFace + README benchmarks
```

---

## Phase 0 — Repo Structure & Plan
**Status: ✅ Done**

- `plan/ROADMAP.md` — this file
- Folder skeleton created: `continual-pretraining/`, `evaluation/`, `finetuning/`

---

## Phase 1 — Continuous Pre-training (CPT)
**File**: `continual-pretraining/01_cpt_llama31_8b.ipynb`  
**Hardware**: Colab 40GB for full run | Local 8GB for config test with 3B  
**Duration**: ~2–3 Colab sessions

### Config
| Setting | Value |
|---|---|
| Base model | `unsloth/Meta-Llama-3.1-8B` |
| Quantization | NF4 4-bit |
| LoRA rank | 64 |
| LoRA alpha | 128 |
| Target modules | q/k/v/o + gate/up/down projections |
| Sequence length | 2048 tokens |
| Batch size | 4 × grad_accum 8 = 32 effective |
| Learning rate | 2e-4, cosine with 5% warmup |
| Epochs | 2 |
| Packing | ✅ (sequences packed for efficiency) |

### Output
HuggingFace: `wickkiey/tamil-llama-3.1-8b-cpt-v1`

---

## Phase 2 — Data Expansion
**File**: `continual-pretraining/02_data_expansion_pipeline.ipynb`  
**Hardware**: Colab (for download + processing speed)  
**All sources free on HuggingFace**

| Dataset | HF path | Size (Tamil) |
|---|---|---|
| CC-100 Tamil | `cc100` lang=ta | ~17GB raw |
| IndicCorp v2 | `ai4bharat/IndicCorp` | ~8GB Tamil shard |
| OSCAR 2301 | `oscar-corpus/OSCAR-2301` | ~3GB Tamil |

Deduplication: MinHash LSH (`datasketch`)  
Quality filter: Tamil Unicode ratio >80%, length >50 chars  
Final mix: 40% Wikipedia + 30% IndicCorp + 20% CC-100 + 10% OSCAR

---

## Phase 3 — Synthetic Instruction Data (Local, Free)
**Files**:
- `evaluation/01_generate_synthetic_local.ipynb` — Ollama on local 8GB machine
- `evaluation/02_batch_generate_colab.ipynb` — batch generation on Colab 40GB

**No API keys needed.** Uses Ollama + Llama 3.1 8B Instruct (4-bit) running locally.

### Generation Templates (all in Tamil)

| Type | Volume | Description |
|---|---|---|
| Q&A extraction | 20K pairs | From Wikipedia article chunks |
| Summarization | 10K pairs | Compress section to 2–3 sentences |
| Fill-in-blank | 10K pairs | Mask named entities, ask to fill |
| Instruction paraphrase | 10K pairs | Article title → "Describe X" format |

**Target: 50K synthetic Tamil instruction pairs**  
Filter: Tamil script ratio >70%, response length >20 chars

---

## Phase 4 — SFT (Supervised Fine-tuning)
**File**: `finetuning/02_sft_instruction_tuning.ipynb`  
**Hardware**: Colab 40GB  
**Starts from**: Phase 1 CPT checkpoint

### Training Data Mix
| Source | Size | Format |
|---|---|---|
| Synthetic Q&A (Phase 3) | 50K | Alpaca |
| `ai4bharat/IndicInstruct` Tamil | ~15K | ShareGPT |
| `ai4bharat/IndicXNLI` Tamil | ~5K | Classification |
| `ai4bharat/IndicSentiment` Tamil | ~5K | Classification |

### Config
- LoRA rank 128, starting from CPT checkpoint
- 3–5 epochs, lr=2e-5

**Output**: `wickkiey/tamil-llama-3.1-8b-sft-v1`

---

## Phase 5 — DPO (Direct Preference Optimization)
**File**: `finetuning/03_dpo_preference_training.ipynb`  
**Hardware**: Colab 40GB  
**Starts from**: Phase 4 SFT checkpoint

### Preference Pair Generation (local, free)
- **Chosen**: SFT model response at temperature 0.3
- **Rejected**: SFT model response at temperature 1.2 (lower quality)
- Additional ranking: Tamil script ratio, response coherence heuristics
- Dataset size: 5K–10K pairs

### Config
- `TRL DPOTrainer`, β=0.1, lr=5e-7, 1–2 epochs

**Output**: `wickkiey/tamil-llama-3.1-8b-dpo-v1`

---

## Phase 6 — RLHF (Later Phase)
**File**: `finetuning/04_rlhf_ppo.ipynb`  
**Trigger**: Only if DPO improvements plateau

1. Train Tamil reward model (Llama 3.2 3B as binary classifier on preference pairs)
2. PPO training with `trl.PPOTrainer`
3. High memory — full Colab 40GB session

**Output**: `wickkiey/tamil-llama-3.1-8b-rlhf-v1`

---

## Phase 7 — Benchmarking vs Sarvam
**File**: `evaluation/03_benchmark_eval.ipynb`

### Tasks via `lm-evaluation-harness`
```
mmlu_ta, arc_challenge_ta, boolq_ta, triviaqa_ta,
xquad_ta, flores_200_ta (translation)
```

### Comparison Matrix
Run all tasks on:
1. Our model (each checkpoint)
2. `sarvamai/sarvam-1` (baseline)
3. `unsloth/Meta-Llama-3.1-8B` (no CPT, sanity check)

---

## Phase 8 — Publication
1. Push all checkpoints to HF with full model cards
2. Update `README.md` with benchmark comparison table
3. GitHub release tags: `cpt-v1`, `sft-v1`, `dpo-v1`

---

## Hardware Reference

| Task | Machine | Config |
|---|---|---|
| Config testing | Local 8GB | Llama 3.2 3B, 4-bit QLoRA |
| CPT training | Colab 40GB | Llama 3.1 8B, 4-bit QLoRA |
| Synthetic data gen (overnight) | Local 8GB | Ollama + Llama 3.1 8B Instruct |
| SFT training | Colab 40GB | LoRA rank 128 |
| DPO training | Colab 40GB | Holds 2 model copies in memory |
| RLHF | Colab 40GB | PPO memory intensive |
| Evaluation | Local 8GB or free Colab | Inference only |

---

## File Index

```
plan/
  ROADMAP.md                                    ← this file
continual-pretraining/
  01_cpt_llama31_8b.ipynb                       ← Phase 1: CPT
  02_data_expansion_pipeline.ipynb              ← Phase 2: Data expansion
evaluation/
  01_generate_synthetic_local.ipynb             ← Phase 3a: Local Ollama gen
  02_batch_generate_colab.ipynb                 ← Phase 3b: Colab batch gen
  03_benchmark_eval.ipynb                       ← Phase 7: Benchmarking
finetuning/
  Tamil Mistral_(7B)-Text_Completion.ipynb      ← existing (text completion)
  02_sft_instruction_tuning.ipynb               ← Phase 4: SFT
  03_dpo_preference_training.ipynb              ← Phase 5: DPO
  04_rlhf_ppo.ipynb                             ← Phase 6: RLHF (stub)
data/
  tawiki_chunked.jsonl                          ← 532K chunks, 845MB
  tawiki_pages.jsonl                            ← 171K full articles
```
