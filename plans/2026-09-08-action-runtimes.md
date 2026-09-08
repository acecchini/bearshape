# Use supported runtimes for artifact and Pages actions


Maintain this ExecPlan according to PLANS.md. This focused CI maintenance PR follows #29 and addresses deprecation warnings observed during the actual release validation run.

## Purpose / Big Picture


The validated release pipeline should not depend on GitHub forcibly substituting a deprecated Node runtime. Update artifact and Pages actions to reviewed immutable Node 24 releases while preserving artifact identity, extraction, environment permissions and the nonpublishing validation path.

## Progress


- [x] (2026-09-08) Created codex/action-runtimes and matching worktree from the handoff candidate.
- [x] (2026-09-08) Verified upstream release tags, action inputs, Node 24 runtime and Pages' embedded artifact upload.
- [x] (2026-09-08) Opened #30 and updated all four reviewed action pins; required docs validation now packages Pages without deployment.
- [x] (2026-09-08) Hooks/actionlint and all PR checks pass. Validation-only run 34223582731 completed 38 jobs successfully and skipped publication; inspected action logs have no Node 20 warning.
- [x] (2026-09-08) Recorded final hashes, 1,101 installed-consumer tests per endpoint, unchanged GPU-validated wheel and inspected 46-file Pages archive.
- [ ] Obtain user validation before merge.

## Surprises & Discoveries


Run 34221337124 succeeded but warned that upload/download-artifact v4 target Node 20 and are forced onto Node 24. Current upstream upload-artifact 7.0.1 and download-artifact 8.0.1 explicitly use Node 24. Download 8 defaults to failing digest mismatches, which strengthens the existing artifact identity check. Upload still archives by default, preserving this workflow's named multi-file artifact contract.

Upload-pages-artifact 5.0.0 uses a pinned upload-artifact 7.0.0 internally. Deploy-pages 5.0.1 uses Node 24. Their existing path, environment and output contracts remain applicable. Hosted GitHub.com runners satisfy the runtime requirement; no self-hosted CI runner is advertised.

## Decision Log


Decision: Update these four actions together in a separate PR with immutable pins. Rationale: the warning concerns the same artifact/deployment runtime transition; feature/runtime implementations remain separate. Date: 2026-09-08.

Decision: Retain archive=true and the existing candidate-distributions name/path. Rationale: installed consumers and publication must download the same wheel/sdist pair. Preserve failure-on-digest-mismatch behavior and never rebuild in the publisher.

Decision: Validate Pages packaging without deploying the site during this task. Rationale: deployment is not required to prove the artifact transition, and the focused PR is unmerged. Existing Pages publication remains governed by its environment and branch event.

## Outcomes & Retrospective


The Node 24 artifact pipeline succeeds end to end. Named artifact upload/download, full installed consumers, release evidence and Pages packaging are verified. The wheel is byte-identical to the artifact that passed 95 GPU tests at both endpoints. Actual Pages deployment was not run. The latest upstream downloader still emits a Buffer() deprecation notice; it is recorded without suppression and does not affect the successful digest/consumer checks. No package behavior, release authorization or ownership controls change. A04 and CuPy static policy remain open decisions.

## Context and Orientation


Worktree /Users/ale/Code/bearshape-worktrees/action-runtimes, branch codex/action-runtimes. .github/workflows/validate.yml builds and distributes the tested artifact. .github/workflows/pypi.yml downloads it for evidence and possible publication. .github/workflows/docs.yml packages and deploys Pages. Dependabot already checks GitHub Actions weekly.

Verified pins: upload-artifact 7.0.1 is 043fb46d1a93c77aae656e7c1c64a875d1fc6a0a; download-artifact 8.0.1 is 3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c; upload-pages-artifact 5.0.0 is fc324d3547104276b827a68afc52ff2a11cc49c9; deploy-pages 5.0.1 is 368f82528645a54fb793d4d04e342629a3f51346.

## Plan of Work


Replace only the four reviewed action references in the three workflows, preserving inputs and job dependencies. Add the Pages artifact packaging step to the already-required documentation validation job so the updated composite upload executes without deployment. Use a distinct validation artifact name to avoid the real github-pages deployment artifact.

Run hooks and actionlint. Push the focused branch, inspect all required hosted checks and dispatch pypi.yml from this branch with publish=false. Verify artifact consumers, evidence hashes and the skipped publisher. Inspect relevant logs for any remaining Node 20 warning on these actions. Record the exact run and artifact identity in this plan; do not claim the Pages deploy job actually ran.

## Concrete Steps


From this worktree run uv run --locked prek run -a and its manual actionlint hook. After pushing, run gh workflow run pypi.yml --ref codex/action-runtimes -f ref=codex/action-runtimes -F publish=false. Read all required job conclusions and download release-evidence plus candidate-distributions for identity verification.

## Validation and Acceptance


The full candidate matrix and validation-only release workflow succeed, with publication skipped. Named artifact extraction and installed consumers remain correct; digest mismatch handling is error by default. Required docs validation successfully packages a Pages artifact with the new composite action. These updated action logs no longer report a Node 20 runtime. Actual Pages/PyPI deployment and user merge approval remain pending.

## Idempotence and Recovery


Only this feature worktree is edited. Do not deploy docs, publish packages, change tags/settings or merge an actual PR base. If a new action contract breaks consumers, inspect the observed behavior and keep publication ineligible until repaired.

## Artifacts and Notes


Record logs under /Users/ale/Code/bearshape-implementation-2026-09-08/evidence/action-runtimes-*. Preserve the earlier release evidence as a separate artifact pair. The complete handoff report remains in docs/maintainers/production-readiness.md.

## Interfaces and Dependencies


No Python dependency or API changes. GitHub Actions pins and the required docs packaging check are the only implementation surface. Keep OIDC write permissions confined to the actual deployment jobs.

Revision note — 2026-09-08: Final validation-only run https://github.com/acecchini/bearshape/actions/runs/34223582731 used source 6f40e4a484b70535c58e2c86a645a64ab1079143. Wheel SHA256 c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2; sdist SHA256 38d89d4ce1b351601ff8602a9a27b4e9af46db056be3ac0eaf41a68ac56a3706. Artifact identity and nondeployment were verified, with owner review still pending.
