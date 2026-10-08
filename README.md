# ROCm 6000 Series Diagnostics

A small Python starter library and command-line tool for inspecting whether a local PyTorch installation was built with ROCm and whether it can see AMD GPUs. For detected devices it reports the name and, when exposed by PyTorch, the GFX architecture string.

This is a **diagnostics helper**, not a ROCm runtime, kernel library, driver installer, or official compatibility validator. It does not decide whether a specific RX 6000-series card is supported. Support depends on the exact GPU, operating system, driver, ROCm release, and PyTorch build; verify that combination against the vendor's current documentation and a real workload.

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

## Compatibility records

Add real test results here only after testing a workload on the complete configuration. Detection alone is not a compatibility test.

| GPU model | Architecture | OS | AMD driver | ROCm | PyTorch build | Workload/result |
| --- | --- | --- | --- | --- | --- | --- |
| Not tested | Not tested | Not tested | Not tested | Not tested | Not tested | Not tested |

## Scope and contributions

Keep the package focused on diagnostics. Do not commit proprietary SDK/runtime binaries, compiled GPU kernels, model weights, or copied application bundles. Include the exact GPU model, OS, driver, ROCm version, PyTorch build, command, and workload with any compatibility report.

## License

No license has been selected yet. Add a license before granting others permission to reuse or distribute this code.