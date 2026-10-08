"""Command-line entry point for the ROCm diagnostics report."""

import json
from dataclasses import asdict

from rocm6000 import inspect_rocm


def main() -> int:
    """Print the diagnostic report as JSON."""
    report = inspect_rocm()
    print(json.dumps(asdict(report), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())