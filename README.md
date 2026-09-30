# Tamil-LLM
LLM for Tamil language

## Training

Follow the [end-to-end training guide](TRAINING.md) to prepare data, run CPT, generate instruction data, perform SFT/DPO, and evaluate checkpoints. See [the roadmap](plan/ROADMAP.md) for target models, phases, and benchmark goals.

## GPU Dev Container (Recommended on Windows)

This repo includes a GPU-enabled VS Code Dev Container using `unsloth/unsloth`.

1. Install Docker Desktop and enable WSL2 backend.
2. Ensure host GPU integration is enabled in Docker Desktop.
3. In VS Code run `Dev Containers: Reopen in Container`.

Dev container files:
- `.devcontainer/devcontainer.json`
- `.devcontainer/requirements.txt`
- `.devcontainer/README.md`
