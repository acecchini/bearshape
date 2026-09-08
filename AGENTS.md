# bearshape agents

bearshape checks runtime array shapes, dtypes and tree constraints through
beartype. Scientific Python developers and library authors use its annotations
at API boundaries alongside native backend types. Keep the public identity
lowercase `bearshape`.

This is the shared Codex/Claude instruction file. `CLAUDE.md` points here.
Human setup and commands live in `CONTRIBUTING.md`; tool usage lives in
`tools/README.md`. Read `docs/maintainers/production-readiness.md` and the
current plan before changing a contract. Historical plans record their original
evidence; current owner decisions take precedence.

## Working rules

- State assumptions before changing behavior. Resolve routine implementation
  choices within the approved scope; ask when a missing decision changes the
  public contract or acceptance criteria.
- Maintenance is now surgical by default. The rename is complete. No speculative
  features, duplicate helpers, unused abstractions or broad cleanup unrelated to
  the requested work.
- Preserve public annotation syntax and useful errors. Use explicit names,
  simple control flow and the existing 2-space Python indentation.
- Keep runtime behavior and static consumer behavior aligned. Passing syntax
  checks, skipped tests and inferred `Any` do not prove support.
- Do not spawn other agents unless the user requests delegation.

## Current release contract

- bearshape is independently versioned; the candidate is `0.1.0rc0`.
- The current dependency and test target is beartype `0.23.0rc0`, with metadata
  `>=0.23.0rc0,<0.24`. Full native composite-union rollback is still incorrect.
  A tested local upstream proposal and explicit integration regressions are
  documented in `tools/upstream/README.md`; it has not shipped upstream.
  The current proposal uses `__beartype_state__` to return the active memo, not
  the superseded snapshot-callback interface. The owner requested optimization
  before upstream contact; local Zulip discussion material is not a sent message.
  The owner chose full composition through supported upstream integration and
  permits a later candidate. Keep rc0 validation until a concrete replacement is
  implemented and tested; update metadata, lock, preflight and CI together.
- Do not replace beartype, monkeypatch upstream internals, infer union boundaries
  from bytecode, hide the defect with an xfail, or restrict composition to make
  CI pass. `tools/probe_union.py` reproduces the open release blocker.
- pyright, mypy, ty and pyrefly are supported through the consumer harness on
  Python 3.10–3.14. New checkers, including zuban, need an explicit plan.
- Native CuPy static typing is explicitly limited, as accepted by the owner.
  Its protocol fallback does not prove native ndarray method inference. Actual
  GPU runtime evidence is recorded separately in the handoff report.
- Release readiness remains withheld until the union integration and release
  prerequisites are satisfied. Merge approval does not authorize publication,
  deployment, access changes, ownership transfer or messages to maintainers.

## Product boundaries

- Root imports must not load NumPy, JAX, Torch, CuPy or optree. Backend behavior
  belongs in its explicit module; do not widen the root API for shorter examples.
- Preserve named, anonymous, fixed, arithmetic and broadcastable dimensions,
  `Scalar`, `Value(...)`, backend aliases, `Like[...]`, scalar-like types and
  `Tree[...]`. Dimensions are runtime constraints, not static shape proofs.
- NumPy owns the broadest dtype/scalar/Like surface. Other backends use their
  own native arrays and selected converters. Like validation does not replace
  the caller's argument or retry failed conversions through a different backend.
- Bare `@check` manages memo scope. Combine it with `@beartype`, or use
  `@check(conf=...)`, to perform type checking.
- Keep runtime tree structure syntax distinct from checker-supported containers.
  optree uses the default registry; there is no custom namespace API.
- `Value` expressions are trusted developer contracts, not a security sandbox.

Memo ownership, frame discovery, failed-alternative rollback, async contexts,
decorator metadata, dtype normalization and static aliases need focused positive
and negative regressions. Preserve lifetime/weak-reference evidence when changing
state ownership. Read the feature-to-test map in the handoff report.

## Major-work workflow

For features, contract changes, packaging, CI, release work and substantial
refactors: create a feature branch and matching worktree, commit an ExecPlan
following `PLANS.md`, and open a PR before implementation. Keep independent
changes in focused PRs and document any dependency on another PR. Use the
existing task goal when one exists; do not start duplicate goals.

Keep the plan current and validate each milestone. Present a concrete result
before requesting merge approval. Reuse explicit approval already given in the
conversation for that scope; do not ask again solely because work crossed a
milestone or worktree. After approval and passing checks, merge, verify main and
remove only clean merged branches/worktrees after preserving evidence.

For stacked PRs, merging a head into its actual base can mark the PR merged.
Before approval, use a separate integration branch to validate combinations.
After approval, preserve every reviewed head in the merged history, including
conflict resolutions; verify reachability before cleanup. Never force main or
delete another contributor's changes. Small, explicitly requested low-risk edits
may skip the major-work workflow.

## Validation

Use the locked uv toolchain. Start with `uv sync --locked`; install hooks with
`uv run --locked prek install`. Use these routes from the repository root:

- Runtime changes: `uv run --locked pytest tests/ --ignore=tests/test_typecheck.py -n auto`.
- Typing changes: `uv run --locked pytest tests/test_typecheck.py -q`; this runs
  all four engines, source checks and real positive/negative/inference consumers
  with interpreter-matched settings. Direct checker commands are debugging aids.
- Normal hooks: `uv run --locked prek run -a`.
- Workflows: `uv run --locked prek run actionlint -a --stage manual`.
- Select relevant tox, docs/notebook, minimal and installed-archive checks from
  `CONTRIBUTING.md` and `tools/README.md`; do not invent environment factors.

Run a failing regression first when practical. Broaden validation when inputs or
unresolved risks justify it, not by repeatedly rerunning unchanged expensive
suites. Do not lower coverage, suppress diagnostics or remove negative fixtures
to obtain green checks. Stage new files before running hooks; review formatting
changes before committing. Git subprocesses targeting a different repository
must clear the names reported by `git rev-parse --local-env-vars`; use the
existing `git_environment` helper for release tooling and its fixtures. Real
hook execution is part of validation when changing lifecycle stages.

CI, nightly and candidate validation share `.github/workflows/validate.yml`.
Required lanes include CPU backends, four checkers, compatibility floors, docs,
notebook and normal installed-wheel consumers. Minimal environments require an
exact sync or a fresh venv; `uv run --only-group` can retain earlier packages.
CuPy needs real CUDA hardware. CPU skips are not GPU evidence, and historical
GPU results do not validate a changed package automatically.

## Docs and handoff

Keep README concise and examples test-backed. Build and inspect changed rendered
structures; execute changed runnable examples and notebook cells. Document
runtime-only syntax and backend/checker limits explicitly. Update CHANGELOG for
features and major user-visible changes.

Record source commits, versions, artifact hashes, commands and meaningful
results in the plan or handoff report. Distinguish implementation completion,
merge state and release readiness. Keep public repository/PyPI/Pages identities
unchanged until the corresponding ownership operation has actually happened.
