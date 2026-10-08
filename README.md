# ROCm 6000 Series Project Template

This repository is a starter template for Python projects targeting AMD GPUs through ROCm and PyTorch, including RX 6000-series hardware where the exact software stack supports it. It includes a small diagnostics library and command-line tool to inspect the local PyTorch/ROCm environment before adding application-specific GPU work.

This template is not itself a ROCm runtime, driver installer, benchmark, or official compatibility validator. Detecting a GPU does not prove that a workload is supported. Support depends on the exact GPU, operating system, driver, ROCm release, and PyTorch build; verify that combination against AMD's current documentation and a real workload.

## What you can build with it

- **Tensor and matrix calculations:** matrix multiplication, vector operations, reductions, and other PyTorch tensor workloads.
- **Image and video processing:** batched image transforms, filters, resizing, and other operations supported by the libraries you add.
- **Machine-learning applications:** model inference or experimentation with ROCm-compatible PyTorch models.
- **Scientific and engineering computing:** numerical workloads that can be expressed with supported PyTorch operations.

These are project directions, not calculations implemented by this starter yet. The code currently provided is the ROCm/PyTorch diagnostics helper described below; add and test your chosen workload in its own module before treating it as part of the library.

## Included

- `rocm6000.inspect_rocm()`: reports whether PyTorch imports, its version and HIP/ROCm version, GPU visibility, GPU names, GFX architecture identifiers when exposed, and diagnostic errors.
- `rocm6000-diagnose`: prints the same report as JSON for setup checks and bug reports.
- Packaging metadata and offline unit tests that do not require an AMD GPU.

The starter does not include matrix-multiplication functions, image/video kernels, machine-learning models, or GPU-specific compiled code. It does not install drivers or ROCm, choose PyTorch wheels, or certify RX 6000-series support.

## Requirements

- Python 3.10 or newer.
- PyTorch with a ROCm build to inspect an AMD GPU. PyTorch's ROCm build uses the `torch.cuda` API; this package deliberately does not install or bundle PyTorch.
- A supported AMD driver and ROCm/PyTorch combination. Follow the current AMD install guide for your operating system: [ROCm on Linux](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/) or [ROCm on Windows](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/).

The report command can also run without PyTorch or a visible GPU and will describe the condition it found. No GPU is needed to run the unit tests.

## Install

From a clone of this repository, install the package in editable mode:

```powershell
python -m pip install -e .
```

Install the PyTorch build that matches your operating system and ROCm setup separately, using the current instructions from AMD or the PyTorch project. Do not install a random ROCm wheel based only on the RX 6000 product family.

## Use

Run the CLI and print a JSON diagnostic report:

```powershell
rocm6000-diagnose
```

Or use the library API:

```python
from dataclasses import asdict
import json

from rocm6000 import inspect_rocm

report = inspect_rocm()
print(json.dumps(asdict(report), indent=2))
```

The report includes whether PyTorch imports successfully, its version, detected HIP/ROCm version, device availability, GPU names, architecture strings when PyTorch exposes them, and diagnostic errors. A missing or broken PyTorch installation or unavailable GPU is reported as data; it is not treated as proof that the hardware is unsupported.

## Test

```powershell
python -m unittest discover -s tests -v
```

Tests use fake PyTorch objects and do not require ROCm hardware.

## Compatibility

The package itself requires Python 3.10 or newer and uses only the Python standard library. It queries PyTorch's `torch.cuda` API, which ROCm-enabled PyTorch also provides. To identify ROCm, it reads `torch.version.hip`; to identify devices, it asks the installed PyTorch build. The package does not have its own GPU backend and does not bundle PyTorch or ROCm.

The project is aimed at diagnostics for AMD GPUs, including Radeon RX 6000-series devices that report GFX103x targets such as `gfx1030`, `gfx1031`, `gfx1032`, or `gfx1034`. These are architecture identifiers the report may display, **not a guarantee** that every card, OS, or ROCm/PyTorch combination can execute workloads. GPU execution support is determined by AMD's support matrix for the exact software versions in use.

| Component or configuration | Compatibility/status |
| --- | --- |
| Python | 3.10 or newer; package source uses the standard library only |
| ROCm-enabled PyTorch | Inspected through `torch.version.hip` and PyTorch's device API; live ROCm runtime not validated in this repository |
| CPU-only PyTorch or no visible GPU | Reported as a diagnostic state; GPU hardware is not needed for unit tests |
| AMD RX 6000 / GFX103x GPU execution | Intended diagnostic audience; no physical-GPU workload has been tested here, so execution compatibility is **unverified** |
| Windows ROCm GPU support | Depends on AMD's supported GPU/driver/ROCm/PyTorch combination; not certified by this project |
| Linux ROCm GPU support | Depends on AMD's supported GPU/driver/ROCm/PyTorch combination; not certified by this project |

Check AMD's current [Linux installation documentation](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/) or [Windows installation documentation](https://rocm.docs.amd.com/projects/install-on-windows/en/latest/) before choosing a GPU, driver, ROCm release, or PyTorch build. Add a compatibility result here only after testing a real workload on the complete configuration; detection alone is not a compatibility test.

## Scope and contributions

Keep the package focused on diagnostics. Do not commit proprietary SDK/runtime binaries, compiled GPU kernels, model weights, or copied application bundles. Include the exact GPU model, OS, driver, ROCm version, PyTorch build, command, and workload with any compatibility report.

## License

No license has been selected yet. Add a license before granting others permission to reuse or distribute this code.