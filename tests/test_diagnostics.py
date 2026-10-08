"""Offline tests for ROCm environment reporting."""

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from rocm6000.diagnostics import inspect_rocm


class InspectRocmTests(unittest.TestCase):
    def test_reports_rocm_build_and_visible_gfx_device(self) -> None:
        torch_module = SimpleNamespace(
            __version__="2.7.0+rocm6.3",
            version=SimpleNamespace(hip="6.3.42131"),
            cuda=SimpleNamespace(
                is_available=lambda: True,
                device_count=lambda: 1,
                get_device_properties=lambda index: SimpleNamespace(
                    name="AMD Radeon RX 6800 XT", gcnArchName="gfx1030"
                ),
            ),
        )

        report = inspect_rocm(torch_module)

        self.assertTrue(report.torch_importable)
        self.assertTrue(report.rocm_enabled)
        self.assertEqual(report.rocm_version, "6.3.42131")
        self.assertTrue(report.device_available)
        self.assertEqual(report.device_count, 1)
        self.assertEqual(report.devices[0].name, "AMD Radeon RX 6800 XT")
        self.assertEqual(report.devices[0].architecture, "gfx1030")

    def test_reports_cpu_only_torch_without_querying_devices(self) -> None:
        torch_module = SimpleNamespace(
            __version__="2.7.0+cpu", version=SimpleNamespace(hip=None)
        )

        report = inspect_rocm(torch_module)

        self.assertTrue(report.torch_importable)
        self.assertFalse(report.rocm_enabled)
        self.assertFalse(report.device_available)
        self.assertEqual(report.device_count, 0)
        self.assertEqual(report.devices, ())

    def test_reports_import_failure(self) -> None:
        with patch(
            "rocm6000.diagnostics.import_module",
            side_effect=ModuleNotFoundError("No module named 'torch'"),
        ):
            report = inspect_rocm()

        self.assertFalse(report.torch_importable)
        self.assertFalse(report.rocm_enabled)
        self.assertIsNone(report.device_available)
        self.assertIn("Could not import PyTorch", report.errors[0])


if __name__ == "__main__":
    unittest.main()