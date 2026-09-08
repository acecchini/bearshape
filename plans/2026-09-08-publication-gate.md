# Publish only the exact validated release artifacts


Maintain this ExecPlan according to PLANS.md. This focused M9 PR builds on aggregate #27. Implementation is authorized; publication, access-control changes and ownership transfer are not.

## Purpose / Big Picture


A release must not bypass runtime, typing, documentation or installed-package validation. Resolve the requested ref to one immutable commit, validate it fully, and publish the exact wheel and source archive that passed. Maintainers also need a validation-only path that produces inspectable evidence without uploading to PyPI.

## Progress


- [x] (2026-09-08) Created codex/publication-gate and matching worktree from 51b5f08.
- [x] (2026-09-08) Inspected current publication workflow, reusable validation, GitHub protection settings and official OIDC guidance.
- [x] (2026-09-08) Opened #28 and implemented matching workflow/tag/commit, version, prerelease and main-ancestry gates.
- [x] (2026-09-08) All 19 real-Git-history tests pass; inspected 128 publication-result combinations and exact artifact/OIDC dependencies.
- [x] (2026-09-08) Full hooks/actionlint and all PR checks pass. Validation-only run 34221337124 succeeded with every required job green and publication skipped.
- [x] (2026-09-08) CONTRIBUTING records the release procedure and inspected/proposed administrative controls.
- [ ] Obtain user review before merge.

## Surprises & Discoveries


The current publish workflow accepts any dispatch ref, builds it and publishes without test dependencies. Main has no branch protection; repository rulesets are empty. The pypi environment allows main branches and v* tags, has no approval reviewers and permits administrator bypass. The github-pages environment allows docs/main branches. These are read-only observations on 2026-09-08; no controls were changed. PyPI trusted-publisher configuration is not verified through the available repository API.

## Decision Log


Decision: Keep release-published events and add dispatch publication defaulting to false. Rationale: validation-only runs should be possible for a branch/commit without making it eligible for publication. Actual publication must use a canonical v<project-version> tag whose commit is already on main and whose event prerelease flag matches the version. Date: 2026-09-08.

Decision: Use the existing reusable validation and its candidate-distributions artifact. Rationale: the wheel tested by minimal and installed consumers must be the wheel published; no second build is allowed. Resolve once and pass the immutable SHA to every checkout. Record archive hashes, version and source SHA separately from the dist directory.

Decision: Keep OIDC write permission only on the final protected pypi job, with pinned actions and no long-lived token. Rationale: build and validation jobs do not need publication credentials. Environment reviewers and tag/main protections are administrative acceptance items, not implied by YAML.

## Outcomes & Retrospective


The release workflow now validates one immutable commit and publishes only its tested artifact pair. The actual validation-only run at 3ee4c1d succeeded, produced provenance and skipped the OIDC publisher. Tests reject branch publication, mismatched versions/prerelease flags/workflow identity, missing or mismatched tags and unmerged commits. A04 native union rollback and CuPy static policy remain release blockers outside this workflow change. A green workflow does not authorize publication or establish unconfigured administrative protections.

## Context and Orientation


Worktree /Users/ale/Code/bearshape-worktrees/publication-gate, branch codex/publication-gate. .github/workflows/pypi.yml is the existing release/dispatch entry point. .github/workflows/validate.yml owns all required CPU, checker, dependency, docs, notebook and artifact jobs. tools/check_distribution.py validates archive metadata and contents. tools/check_installed.py consumes copies of downstream tests outside src. pyproject.toml declares 0.1.0rc0 and beartype >=0.23.0rc0,<0.24.

## Plan of Work


Add a small release validation tool that reads the event and resolved repository state, validates the canonical tag/version relationship for publication and prerelease status, and emits JSON plus GitHub job outputs. Use argument-list subprocess calls and strict ref handling; reject branch publication, mismatched versions, unresolved tags and tags outside main history. Permit arbitrary repository refs only in validation-only mode.

Refactor pypi.yml into resolve, reusable validation, evidence and publish jobs. The evidence job consumes the existing distributions, checks their metadata version against the resolved project version, and records SHA256/source commit/run URL. Publish downloads those same immutable artifacts and needs successful validation and evidence. Validation-only runs skip publication explicitly.

Add focused tests for valid rc/final releases and rejected branch, mismatch, prerelease and ancestry cases. Validate the workflow graph and failed-required-job exclusion without uploading anything. Keep source-archive consumer tests runnable when they reference the release helper. Document the command, release procedure and concrete settings still requiring the owner's authorization.

## Concrete Steps


From this worktree run targeted pytest for release validation, then uv run --locked prek run -a and its manual actionlint stage. Exercise the release tool with temporary Git repositories and synthetic GitHub event files. Build and inspect artifacts, then run the hosted candidate matrix. Exercise a validation-only dispatch only if GitHub can run this branch workflow without merging it; otherwise record that platform constraint and use the PR-hosted equivalent plus local event tests.

## Validation and Acceptance


A branch or version/prerelease mismatch must fail before publication eligibility. A tag outside main history must fail. Every required validation job must succeed for the immutable SHA. Published artifact selection must refer to the validated artifact without rebuilding. Evidence must contain source SHA, version, wheel/sdist hashes and run link. Validation-only mode must never enter the OIDC publisher job. Actual publishing and administrative settings remain pending explicit authorization.

## Idempotence and Recovery


Use temporary Git repositories for destructive tag/ancestry tests. Never create release tags in the real repository, publish GitHub releases, upload packages, change controls or transfer ownership during validation. Preserve diagnostic logs and retry only understood failures. Main and focused PR branches remain untouched.

## Artifacts and Notes


Store local evidence under /Users/ale/Code/bearshape-implementation-2026-09-08/evidence/publication-*. Record exact GitHub protection observations and proposed controls in the handoff documentation. Archive hash evidence is separate from the files passed to PyPI.

## Interfaces and Dependencies


Use the standard library and existing locked uv tools. Keep the supported Python package range unchanged. GitHub Actions uses immutable action pins, the local reusable validation workflow, artifact upload/download, and pypa/gh-action-pypi-publish with environment pypi and job-scoped id-token: write. No new runtime dependency.

Revision note — 2026-09-08: Verified the actual validation-only workflow at https://github.com/acecchini/bearshape/actions/runs/34221337124. Source 3ee4c1d8a0c3d22f537a24b447a9d75e025a5b2d; wheel SHA256 c1806203da013c9eaf2482a309c686a984c0a7031a495efbd100a824536b57d2; sdist SHA256 e2454095144fb4bb5a08d3bd998d0f6a8bee4bc5ad81dfab763c339ca91666df. Administrative protections remain unconfigured and publication unauthorized.
