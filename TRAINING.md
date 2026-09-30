# End-to-End Training Guide

This guide runs the Tamil LLM pipeline from corpus preparation through evaluation. The notebooks are the executable source of truth; `plan/ROADMAP.md` explains the goals and target scores.

## 1. Prepare the environment

Use an NVIDIA GPU. An A100 40 GB is recommended for full 8B training; an 8 GB GPU is suitable only for the 3B smoke-test configuration.

- **Dev Container:** install Docker, NVIDIA GPU support, and VS Code Dev Containers, then choose **Dev Containers: Reopen in Container**. See `.devcontainer/README.md`.
- **Colab:** select a GPU runtime and open the required notebook. Each notebook installs its dependencies.
- **Hugging Face:** accept the Llama model license, create a write token, and log in with `huggingface-cli login` or set the notebook's `HF_TOKEN` variable at runtime. Never commit a token.

Verify the GPU before training:

```bash
python3 -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

Unsloth is the preferred model loader, inference accelerator, and trainer. TRL is retained for algorithms such as DPO and PPO; importing Unsloth first enables its TRL patches.

## 2. Prepare the Tamil corpus

The default CPT notebook reads `wickkiey/tamil-wikipedia-chunked`. To rebuild it:

1. Run the preprocessing notebooks in `preprocessing/` in filename order.
2. Confirm `data/tawiki_chunked.parquet` exists.
3. Follow `tohf_chunkeddataset/UPLOAD_GUIDE.md` to publish the dataset, or set `HF_DATASET = None` in the CPT notebook and provide `data/tawiki_chunked.jsonl`.

The `data/` directory is intentionally ignored by Git.

## 3. Run Wikipedia continual pre-training

Open `continual-pretraining/01_cpt_llama31_8b.ipynb` and run every cell in order.

- Keep `LOCAL_TEST = True` for a short Llama 3.2 3B smoke test.
- Set `LOCAL_TEST = False` for the planned Llama 3.1 8B run.
- For a full run, confirm `HF_DATASET`, `OUTPUT_DIR`, `HF_REPO`, and `HF_TOKEN` before starting.
- Expected published checkpoint: `wickkiey/tamil-llama-3.1-8b-cpt-v1`.

Check that training loss is finite, a checkpoint exists under `outputs/cpt_v1`, and the final Tamil generation cell produces coherent text.

## 4. Optionally expand the corpus and repeat CPT

Run `continual-pretraining/02_data_expansion_pipeline.ipynb` to combine Wikipedia, IndicCorp, CC-100, and OSCAR data into `wickkiey/tamil-corpus-expanded`.

Then rerun `continual-pretraining/01_cpt_llama31_8b.ipynb` with:

- `HF_DATASET = "wickkiey/tamil-corpus-expanded"`
- `MODEL_NAME` set to the Phase 1 CPT checkpoint
- new `OUTPUT_DIR` and `HF_REPO` values, such as `outputs/cpt_v2` and `wickkiey/tamil-llama-3.1-8b-cpt-v2`

Use the resulting v2 checkpoint for SFT. Do not overwrite the Phase 1 checkpoint.

## 5. Generate instruction data

Choose one or combine both:

- **Local:** run `evaluation/01_generate_synthetic_local.ipynb` with Ollama.
- **Colab:** run `evaluation/02_batch_generate_colab.ipynb`, which uses Unsloth batch inference.

Both paths produce Alpaca-style records with `instruction`, `input`, and `output` fields and can publish them to `wickkiey/tamil-synthetic-instructions`. Inspect samples and verify Tamil-script and response-length filters before publishing.

## 6. Run supervised fine-tuning

Open `finetuning/02_sft_instruction_tuning.ipynb`.

1. Set `CPT_CHECKPOINT` to the latest CPT checkpoint.
2. Verify the synthetic and AI4Bharat datasets load successfully.
3. Run all cells to train with `UnslothTrainer`.
4. Review the sample generations, then save or publish `wickkiey/tamil-llama-3.1-8b-sft-v1`.

## 7. Run preference training

Open `finetuning/03_dpo_preference_training.ipynb`.

1. Set `SFT_CHECKPOINT` to the Phase 4 output.
2. Generate and inspect the chosen/rejected pairs.
3. Run DPO training and the final inference check.
4. Save or publish `wickkiey/tamil-llama-3.1-8b-dpo-v1`.

The notebook uses TRL's DPO API after loading the model with Unsloth, so Unsloth's patches remain active.

## 8. Treat PPO as optional

Run `finetuning/04_rlhf_ppo.ipynb` only if DPO evaluation plateaus. It trains a reward model and then applies PPO, requiring substantially more GPU memory. Keep the DPO checkpoint as the policy input and publish PPO output separately.

## 9. Evaluate and publish

Run `evaluation/03_benchmark_eval.ipynb`.

1. Update its model map with the CPT, SFT, and DPO checkpoints to compare.
2. Run Tamil perplexity and the available lm-evaluation-harness tasks.
3. Compare against Sarvam-1 and the untouched base model.
4. Preserve the generated JSON results and add verified scores to the model card and repository README.

Before publishing a checkpoint, confirm:

- training completed without NaN/Inf loss;
- Tamil sample generations are coherent and do not merely copy prompts;
- the intended adapter and tokenizer reload in a fresh session;
- benchmark settings and dataset revisions are recorded;
- dataset licenses and Tamil Wikipedia attribution are included.

## Recovery and troubleshooting

- **Out of memory:** reduce `BATCH_SIZE` first, increase `GRAD_ACCUM` to retain the effective batch size, then reduce sequence length if necessary.
- **Colab disconnect:** save checkpoints to Drive and resume from the latest `checkpoint-*` directory.
- **Gated model error:** accept the model license and supply a Hugging Face read token.
- **Dataset error:** verify the repository name and expected `text` field before training.
- **Resume safely:** keep checkpoint repository names unique per phase and corpus version.
