# Repair rendered documentation and executable examples


Maintain this ExecPlan according to `PLANS.md`. This focused documentation PR is stacked on integration draft #22 and implements the documentation portion of M8. Artifact installation and publication gating remain separate work.

## Purpose / Big Picture


Users must be able to read rendered shape/casting tables, distinguish runtime checks from static types, and run the documented examples on the Python 3.10 floor. Correct a build that currently succeeds while flattening tables and admonitions and leaving stale claims after the implementation fixes.

## Progress


- [x] (2026-09-08) Created isolated documentation branch/worktree.
- [ ] Open draft PR and reproduce formatter behavior with valid syntax.
- [ ] Repair malformed tables/admonitions and stale examples/support claims.
- [ ] Execute representative docs examples and the example notebook.
- [ ] Verify rendered HTML structures and inspect representative pages visually.
- [ ] Prove formatting is stable, build docs and record evidence.
- [ ] Obtain user validation before merge.

## Surprises & Discoveries


The current docs contain flattened tables (`| |` between intended rows) and admonition text outside the required indentation. A successful Zensical build does not detect this. The installed hook pins mdformat-mkdocs 5.2.0b2 and explicitly selects mkdocs/frontmatter; first test whether the current formatter corrupts valid syntax or whether the malformed input is historical damage. The combined Like guide also retains one stale backend-only static claim despite the corrected aliases.

## Decision Log


Decision: Test a valid formatting round trip before changing formatter dependencies. Rationale: avoid speculative tool upgrades if repairing historical source damage is enough. Date: 2026-09-08.

Decision: Use Python 3.10-compatible aliases and test-backed examples; remove fixed coverage badges and missing asset references. Rationale: docs are user contracts and should not show metrics or syntax the selected environment cannot support.

Decision: Preserve explicit runtime-only syntax and CuPy's observed typing limitations without declaring an unresolved support policy accepted. Rationale: runtime metadata checks and static backend stubs establish different guarantees.

## Outcomes & Retrospective


Implementation pending. Rendered document structure, executable behavior and formatter stability must all be checked; a build exit code alone is insufficient.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/docs-contract`, branch `codex/docs-contract`, base integration `b2a1df0`. `docs/features/` contains dimensions, Like, Tree, decoration and static guides. `docs/getting-started/` owns installation and quickstart. `zensical.toml` defines navigation/assets and markdown extensions. `README.md` is the concise entry point. The example notebook contains 29 code cells according to the audit; inspect actual contents before execution.

## Plan of Work


Probe the pinned formatter on a minimal valid table and admonition, saving original/formatted text. Correct its configuration only if this round trip fails. Restore each damaged table and admonition in source, retaining intended content and reviewing cell boundaries. Repair stale static Like/Tree descriptions, Python 3.12-only aliases in floor-compatible examples, and misleading bare check examples. Keep intentional expected failures clearly labeled.

Execute representative examples in an isolated process using the current candidate, with assertions for valid output and expected rejection. Execute the notebook from a disposable copy, inspect errors and outputs, and update the source only where behavior or claims require it. Build docs with the locked docs-only group. Inspect actual HTML for table rows, admonitions and referenced assets, then visually inspect representative built pages. Re-run all hooks and build to establish a stable round trip.

## Concrete Steps


Use external probe/output files under the implementation evidence directory. From this worktree run:

    uv run --locked prek run -a
    uv run --locked --only-group docs zensical build --clean

Use a separate candidate runtime environment for examples so a docs-only build does not accidentally imply backend validation. Record actual Python/backend versions and rendered checks.

## Validation and Acceptance


Tables render with the expected headers/rows; admonitions render as structured blocks; referenced local assets exist. Maintained examples use supported Python syntax and demonstrate the documented runtime/static contract. The notebook executes without unexpected errors. Hooks leave tracked files unchanged after formatting and the docs-only build succeeds. No full static shape inference or native CuPy stub completeness is promised.

## Idempotence and Recovery


Work only in the isolated branch. Do not overwrite the original audit or unreviewed notebook outputs. Store execution copies/screenshots outside the repository unless they serve a maintained test. Do not deploy the candidate documentation or change organization URLs before ownership transfer.

## Artifacts and Notes


Evidence belongs under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/docs-*`. Keep formatter before/after files, example/notebook output summaries and rendered validation results.

## Interfaces and Dependencies


Use the existing Zensical documentation system and public bearshape API. Add no runtime dependency. Any additional formatter or execution tooling belongs in the appropriate development group or an isolated validation environment and must have a demonstrated use.
