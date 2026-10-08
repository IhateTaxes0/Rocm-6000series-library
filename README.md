# ROCm 6000 Series Library (Template)

> **Status: template only.** This repository currently contains no executable library, GPU kernels, or ROCm runtime. It is a clean starting point for building and documenting a small compatibility/helper library for AMD RDNA 2 (GFX103x) GPUs, including Radeon RX 6000-series cards.

## What this project is intended to do

The planned library will make it easier for an application to report whether its GPU architecture and installed ROCm components match a tested configuration. It should provide a small, documented API and an explicit compatibility matrix. It is not a replacement for AMD's driver or ROCm SDK, and it does not include PyTorch or other framework builds.

Hardware support must be verified per card, operating system, driver, ROCm version, and framework build. The presence of GFX103x packages in another application's distribution is not proof that every RX 6000-series card or operating system is supported.

## Requirements

- An AMD GPU and operating system supported by the specific ROCm release you intend to use.
- A matching AMD driver and ROCm installation. Follow AMD's current installation guide for your platform: <https://rocm.docs.amd.com/projects/install-on-linux/en/latest/> or <https://rocm.docs.amd.com/projects/install-on-windows/en/latest/>.
- A development toolchain for the language chosen for this library. This template does not prescribe one yet.

## Start here

1. Clone this repository and create a feature branch.
2. Decide the library's language, supported platforms, and public API before adding implementation code.
3. Check the GPU model and architecture target with the tools shipped by your ROCm installation. Record the exact command and output in the compatibility table; do not infer compatibility from the product family alone.
4. Add a minimal implementation and tests that run on both a supported ROCm device and a machine without ROCm, where practical.
5. Document installation, build, test, and usage commands here once those commands exist.

## Compatibility matrix

Replace this example row only after testing the complete configuration with a real workload.

| GPU model | Architecture target | OS | Driver | ROCm | Framework/build | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Not tested | Not tested | Not tested | Not tested | Not tested | Not tested | Not tested |

## Repository contents

- `README.md`: project scope, setup prerequisites, and the compatibility record to maintain.
- `.gitignore`: excludes local environments, build output, and packaged GPU/runtime binaries.

Only commit source code, tests, and documentation that you have permission to redistribute. Do not copy the `_rocm_sdk_core`, `_rocm_sdk_libraries_gfx103X_dgpu`, PyTorch, or model-weight folders from an installed application into this repository. Use AMD's official distribution channels for ROCm components and check each dependency's license before redistributing it.

## Contributing

Before reporting a compatibility result, include the exact GPU model, architecture target, OS version, AMD driver, ROCm version, framework build (if used), test command, and observed result. Mark untested combinations as **Not tested** rather than implying support.

## License

Choose and add a license before distributing code. Until a license is added, all rights are reserved by default; do not assume this template grants permission to reuse third-party code or assets.