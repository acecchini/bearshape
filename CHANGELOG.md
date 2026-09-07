# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A GitHub Actions workflow for trusted publishing to PyPI, with automatic
    release-based publishing and manual `workflow_dispatch` support for a chosen
    ref.
- `typing_extensions>=4.6` as a runtime dependency, so the typing constructs
    used by the backend aliases resolve on every supported Python version.

### Fixed

- Backend array aliases (`Shaped`, `F32`, `IntLike`, …) no longer break type
    checkers resolving Python 3.10 or 3.11. The aliases used
    `typing.TypeAliasType` (3.12+) and `typing.TypeVarTuple` (3.11+); they now
    use the `typing_extensions` backports, along with `typing_extensions.Self`
    in `bearshape.cupy` and `typing_extensions.Never` in
    `bearshape._dimensions`.

### Changed

- CI lint and formatting now use the Ruff version in `uv.lock`, avoiding
    unreviewed tool upgrades that disagree with local checks.

- Default type checks now target Python 3.10, with compatibility tests covering
    every supported Python target from 3.10 through 3.14 for pyright, mypy, and
    ty.

- Renamed the distribution, import package, documentation, examples, tests, and
    release metadata to bearshape.

- Normalized product-facing branding to lowercase `bearshape`.

- Switched the documentation build from direct MkDocs usage to Zensical while
    preserving the existing Material-style site proportions and theme.

- Hardened nearest-wrapper memo and scope resolution for plain `@beartype` usage
    in decorated call stacks.

- Hardened standalone `is_bearable()` memo identity against recycled checker
    frame objects.

- Array and tree runtime hints now report readable validation failures through
    custom beartype diagnostics instead of boolean-only validator output.

- Backend `Like[...]` diagnostics now identify JAX, PyTorch, and CuPy hints with
    their owning `bearshape` backend module instead of `numpy`.

## [0.0.1] - 2026-03-31

### Added

- Runtime shape and dtype validation for NumPy, JAX, PyTorch, and CuPy arrays,
    powered by `typing.Annotated` and beartype validators.
- Symbolic dimension syntax including named dimensions, anonymous dimensions,
    `Scalar`, arithmetic dimension expressions, and constrained `Value(...)`
    checks.
- `Tree[...]` validation helpers, explicit `@bearshape.check` support, and
    `check_context()` for shared manual bearability checks.
- Multi-checker typing coverage across pyright, mypy, and ty, with CI, tox, and
    pre-commit validation for runtime and typing behavior.
- A documentation website covering installation, API boundaries, supported
    backends, and practical usage patterns.

### Notes

- The root `bearshape` module intentionally stays lightweight and
    optional-dependency-safe; backend-specific aliases and factories live in
    `bearshape.numpy`, `bearshape.jax`, `bearshape.torch`, and `bearshape.cupy`.
- CuPy support remains optional at install time and requires a compatible CuPy
    environment when used at runtime.
