"""Inspect the local PyTorch ROCm runtime without installing dependencies."""

from dataclasses import dataclass
from importlib import import_module
from typing import Any


@dataclass(frozen=True)
class GpuInfo:
    """Details reported by PyTorch for one visible GPU."""

    index: int
    name: str
    architecture: str | None


@dataclass(frozen=True)
class RocmReport:
    """ROCm and GPU visibility facts reported by the local PyTorch install."""

    torch_importable: bool
    torch_version: str | None
    rocm_version: str | None
    rocm_enabled: bool
    device_available: bool | None
    device_count: int | None
    devices: tuple[GpuInfo, ...]
    errors: tuple[str, ...]


def inspect_rocm(torch_module: Any | None = None) -> RocmReport:
    """Inspect PyTorch's ROCm build and visible devices.

    `torch_module` is an injectable module-like object for testing. When omitted,
    this function imports the installed ``torch`` package.
    """
    errors: list[str] = []
    if torch_module is None:
        try:
            torch_module = import_module("torch")
        except Exception as exc:
            return RocmReport(
                torch_importable=False,
                torch_version=None,
                rocm_version=None,
                rocm_enabled=False,
                device_available=None,
                device_count=None,
                devices=(),
                errors=(f"Could not import PyTorch: {type(exc).__name__}: {exc}",),
            )

    torch_version = getattr(torch_module, "__version__", None)
    rocm_version = getattr(getattr(torch_module, "version", None), "hip", None)
    rocm_enabled = bool(rocm_version)
    if not rocm_enabled:
        return RocmReport(
            torch_importable=True,
            torch_version=torch_version,
            rocm_version=None,
            rocm_enabled=False,
            device_available=False,
            device_count=0,
            devices=(),
            errors=(),
        )

    try:
        device_available = bool(torch_module.cuda.is_available())
    except Exception as exc:
        errors.append(f"Could not query device availability: {type(exc).__name__}: {exc}")
        return RocmReport(
            torch_importable=True,
            torch_version=torch_version,
            rocm_version=str(rocm_version),
            rocm_enabled=True,
            device_available=None,
            device_count=None,
            devices=(),
            errors=tuple(errors),
        )

    if not device_available:
        return RocmReport(
            torch_importable=True,
            torch_version=torch_version,
            rocm_version=str(rocm_version),
            rocm_enabled=True,
            device_available=False,
            device_count=0,
            devices=(),
            errors=(),
        )

    try:
        device_count = int(torch_module.cuda.device_count())
    except Exception as exc:
        return RocmReport(
            torch_importable=True,
            torch_version=torch_version,
            rocm_version=str(rocm_version),
            rocm_enabled=True,
            device_available=True,
            device_count=None,
            devices=(),
            errors=(f"Could not query device count: {type(exc).__name__}: {exc}",),
        )

    devices: list[GpuInfo] = []
    for index in range(device_count):
        try:
            properties = torch_module.cuda.get_device_properties(index)
            architecture = getattr(properties, "gcnArchName", None)
            if architecture is None:
                architecture = getattr(properties, "gcn_arch_name", None)
            devices.append(
                GpuInfo(
                    index=index,
                    name=str(getattr(properties, "name", "Unknown AMD GPU")),
                    architecture=str(architecture) if architecture else None,
                )
            )
        except Exception as exc:
            errors.append(
                f"Could not inspect device {index}: {type(exc).__name__}: {exc}"
            )

    return RocmReport(
        torch_importable=True,
        torch_version=torch_version,
        rocm_version=str(rocm_version),
        rocm_enabled=True,
        device_available=True,
        device_count=device_count,
        devices=tuple(devices),
        errors=tuple(errors),
    )