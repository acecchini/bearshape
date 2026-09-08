# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Require runtime and four-checker consumer tests from normally installed
    sdist-derived wheels outside the checkout on Python 3.10 and 3.14.

- Share candidate validation across PRs, pushes and nightly runs, with explicit
    CPU backends, four checkers, complete hooks and a required final gate.

- Preserve Markdown tables through the formatting hook and restore rendered
    tables/admonitions. Align typing, memo and example guidance with the
    candidate.

- Accept ordinary convertible inputs in static Like annotations: NumPy numeric
    casting families and JAX/Torch scalars, arrays and nested sequences.
    Preserve native result types after explicit conversion.

- Allow nonnumeric NumPy dtypes in static Shaped and ShapedLike annotations.

- Replace nominal static Tree stubs with a shared model for ordinary typed
    leaves, lists, tuples and dictionaries, preserving expected leaf errors.
    Document the concrete-type alias pattern for custom JAX nodes.

- Verify real consumer calls, inferred types, and expected errors with pyright,
    mypy, ty, and pyrefly; require selected tools instead of silently skipping
    them.

- Update the locked checker versions and make `check(conf=None)` match its
    public overloads.

- Include LICENSE in wheel/source distributions and ship the regression suite
    and its configuration in the source archive. Verify actual archive contents.

- Maintain JAX jit/vmap/grad and Torch autograd/compiler-boundary tests, with
    explicit tracing and compilation guidance.

- Verify a normally installed wheel and custom array factory without optional
    backend dependencies on Python 3.10 and 3.14.

### Maintenance

- Align shared Codex/Claude guidance, execution-plan policy, contributor
    commands and tool documentation with the four-checker production validation
    workflow.
- Record the accepted full-union upstream integration path and limited native
    CuPy static support; retain a runnable probe for the open union defect.
- Build documentation on pushes while requiring explicit manual dispatch for
    Pages deployment; scope Pages/OIDC write permissions to that job.

### Added

- Add the production contract/test map, reproducible runtime measurements and
    ownership handoff evidence with unresolved release decisions stated
    explicitly.

- Add CUDA runtime evidence for CuPy conversion, native device/stream
    preservation and optree containers on the corrected candidate.

- A GitHub Actions workflow for trusted publishing to PyPI, with automatic
    release-based publishing and manual `workflow_dispatch` support for a chosen
    ref.

- `typing_extensions>=4.6` as a runtime dependency, so the typing constructs
    used by the backend aliases resolve on every supported Python version.

### Fixed

- `bearshape_this_package()` now instruments the calling package correctly,
    including annotated parameters and returns in subsequently imported modules.

- Validation state now belongs to its active invocation. Failed boolean
    composite checks no longer poison later checks of the same object or retain
    failed arrays through cached annotation state. Diagnostic checks preserve
    the current call's dimension bindings and restore temporary changes.

- Backend `Like` checks now reject inputs that their selected converter cannot
    handle, including unsupported NumPy layouts, byte order, dtypes, and foreign
    protocols. Foreign arrays no longer bypass JAX/Torch/CuPy conversion, and a
    failed backend converter is no longer masked by a NumPy fallback.

- Structured dtype normalization now exposes its NumPy input type to all
    supported checkers while retaining NumPy's runtime validation.

- Backend array aliases (`Shaped`, `F32`, `IntLike`, …) no longer break type
    checkers resolving Python 3.10 or 3.11. The aliases used
    `typing.TypeAliasType` (3.12+) and `typing.TypeVarTuple` (3.11+); they now
    use the `typing_extensions` backports, along with `typing_extensions.Self`
    in `bearshape.cupy` and `typing_extensions.Never` in
    `bearshape._dimensions`.

### Changed

- Update artifact and Pages actions to reviewed Node 24 releases and exercise
    Pages packaging in required documentation validation.

- Require immutable tag/version identity and full candidate validation before
    publishing the tested artifacts; add a validation-only release path.

- Prepare `0.1.0rc0` with beartype `>=0.23.0rc0,<0.24`; older beartype versions
    are no longer supported. Compatibility jobs test the exact rc0 dependency,
    including Python 3.10 and 3.14 CPU backend environments.

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
