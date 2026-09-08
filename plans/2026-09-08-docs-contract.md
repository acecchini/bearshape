# Repair rendered documentation and executable examples


Maintain this ExecPlan according to `PLANS.md`. This focused documentation PR is stacked on CI PR #23 (which uses integration draft #22) and implements the documentation portion of M8. Artifact installation and publication gating remain separate work.

## Purpose / Big Picture


Users must be able to read rendered shape/casting tables, distinguish runtime checks from static types, and run the documented examples on the Python 3.10 floor. Correct a build that currently succeeds while flattening tables and admonitions and leaving stale claims after the implementation fixes.

## Progress


- [x] (2026-09-08) Created isolated documentation branch/worktree.
- [x] (2026-09-08) Opened draft PR #24; reproduced table corruption with the pinned formatter and fixed it with explicit gfm 1.0.0.
- [x] (2026-09-08) Restored ten tables/seven malformed admonitions, corrected typing/memo guidance, and replaced Python 3.12-only alias syntax.
- [x] (2026-09-08) All 29 notebook cells execute on Python 3.10.20 and 3.14.5 with exact candidate dependencies; 92 doc snippets parse at the Python floor.
- [x] (2026-09-08) Executed all five guide example blocks plus scalar dot on both Python endpoints, including valid results and expected violations.
- [x] (2026-09-08) Maintained checker validates expected table rows, admonitions, favicon and snippet syntax; visually inspected the casting table and Boolean warning in the local browser.
- [x] (2026-09-08) Hook formatting round trip and docs-only build pass; notebook outputs and formatter before/after evidence retained externally.
- [x] (2026-09-08) Shared hosted validation including docs and both notebook endpoints passes in run 34218035673 at f8d582b. The simultaneous earlier run was cancelled after the PR base changed.
- [ ] Obtain user validation before merge.

## Surprises & Discoveries


The current docs contain flattened tables (`| |` between intended rows) and admonition text outside the required indentation. A successful Zensical build does not detect this. The installed hook pins mdformat-mkdocs 5.2.0b2 and explicitly selects mkdocs/frontmatter; first test whether the current formatter corrupts valid syntax or whether the malformed input is historical damage. The combined Like guide also retains one stale backend-only static claim despite the corrected aliases.

## Decision Log


Decision: Test a valid formatting round trip before changing formatter dependencies. Rationale: avoid speculative tool upgrades if repairing historical source damage is enough. Date: 2026-09-08.

Decision: Use Python 3.10-compatible aliases and test-backed examples; remove fixed coverage badges and missing asset references. Rationale: docs are user contracts and should not show metrics or syntax the selected environment cannot support.

Decision: Preserve explicit runtime-only syntax and CuPy's observed typing limitations without declaring an unresolved support policy accepted. Rationale: runtime metadata checks and static backend stubs establish different guarantees.

## Outcomes & Retrospective


The pinned formatter originally flattened a valid table. Explicit gfm support preserves it. Ten restored tables and eight rendered admonitions now pass semantic checks. The original notebook failed on Python 3.10 at its Python 3.12 alias syntax; the corrected notebook executes all 29 cells at both Python endpoints, including expected violations that now assert the precise exception. Fixed the broadcast token, native notebook await and previously hard-coded endian results. Cleared stale committed output and added a repeatable kernel runner.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/docs-contract`, branch `codex/docs-contract`, base CI PR #23 at `f396e72`. `docs/features/` contains dimensions, Like, Tree, decoration and static guides. `docs/getting-started/` owns installation and quickstart. `zensical.toml` defines navigation/assets and markdown extensions. `README.md` is the concise entry point. The example notebook contains 29 code cells according to the audit; inspect actual contents before execution.

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

Revision note — 2026-09-08: Stacked on CI PR #23 to add semantic docs and endpoint notebook jobs to shared validation. Kept outputs per interpreter under build/ and enabled only the development notebook dependency group for execution.

Revision note — 2026-09-08: Actual five guide blocks and scalar-dot consumer checks pass on both endpoints; shared hosted run 34218035673 passes with required notebook/docs jobs.
