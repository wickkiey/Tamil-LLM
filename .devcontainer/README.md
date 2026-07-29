# Dev Container (GPU)

This repo is configured to run inside a GPU-enabled Dev Container using the official `unsloth/unsloth` image.

## Prerequisites on Windows

1. Install Docker Desktop.
2. Enable WSL2 backend in Docker Desktop.
3. Enable GPU support in Docker Desktop and ensure `nvidia-smi` works on host.

Reference:
- https://unsloth.ai/docs/get-started/install/windows-installation
- https://docs.docker.com/desktop/features/gpu/

## Open in Container

1. Open this folder in VS Code.
2. Run command: `Dev Containers: Reopen in Container`.
3. After build completes, open notebooks and select the Python kernel from the container.

## Quick GPU Check Inside Container

```bash
python3 -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"
```

If `True` is printed, the container has GPU access.
