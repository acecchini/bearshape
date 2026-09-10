# Restore bearshape after transfer to beartype


This ExecPlan follows `PLANS.md` and is maintained throughout this repair.

## Purpose / Big Picture


Restore the documentation at https://beartype.github.io/bearshape/ and make repository links, installation metadata, and maintainer procedures use the verified new owner, `beartype/bearshape`. The user explicitly requested restoration and all repository repairs caused by the transfer on 2026-09-10. This authorizes the focused repair, merge after passing validation, and Pages deployment. It does not authorize publishing a package or changing unrelated access controls.

## Progress


- [x] (2026-09-10) Confirmed repository transfer, administrator access, active Actions, workflow-based Pages, and existing main/docs deployment policy.
- [x] (2026-09-10) Updated the local origin and created `codex/ownership-transfer` in `/private/tmp/bearshape-ownership-transfer` from main `795ec39`.
- [x] (2026-09-10) Dispatched existing main Pages workflow to restore service while preparing corrected metadata.
- [x] (2026-09-10) Committed plan at `951daae` and opened PR #36 before implementation.
- [x] (2026-09-10) Corrected active links, package metadata and current maintainer guidance; preserved authorship and historical plans.
- [x] (2026-09-10) Validated rendered docs, both archives' metadata, normal hooks and visual homepage preview; initial plan push also passed runtime and four-checker hooks.
- [ ] Hosted CI on the final repair head.
- [ ] Merge repair, deploy corrected main, verify live pages/assets and clean merged worktree.

## Surprises & Discoveries


GitHub reports the new Pages URL and workflow build mode, but no deployment status. The docs workflow deploys only on explicit dispatch; normal main pushes only build artifacts. Existing repository and Pages references still name the former owner. GitHub redirects transferred repository links, but does not redirect Pages sites. Actions are enabled with allowed actions set to all. The Pages environment permits main/docs. No repository Actions secrets or webhooks are configured.

## Decision Log


- Decision: Restore current main immediately through the existing dispatch workflow, then deploy corrected main after validation.
  Rationale: The user's first priority is a working website; the current content can be restored before correcting canonical and repository links.
  Date/Author: 2026-09-10, Codex.
- Decision: Preserve authorship, copyright, historical plan transcripts, runtime APIs, dependency pins and manual publication/deployment gates.
  Rationale: These do not change through a GitHub ownership transfer. Current public links and current handoff status do change. PyPI publisher identity is an external setting and must not be represented as fixed by repository edits.
  Date/Author: 2026-09-10, Codex.

## Outcomes & Retrospective


The initial main dispatch restored the new Pages site (HTTP 200); the old Pages address returns 404. Active documentation, repository/edit/notebook links, package metadata and local origin now identify beartype. Authorship and historical plans are unchanged. All local repair checks pass. Final hosted validation, merge and corrected-site deployment are the remaining execution steps; record their exact run URLs in PR #36. PyPI publisher trust remains external and unverified, and published 0.0.1 retains old URL metadata. The unrelated native union integration remains a release blocker.

## Context and Orientation


`zensical.toml` controls the generated site URL, repository navigation and edit links. `README.md` links to hosted guides. `pyproject.toml` supplies URLs embedded in built Python packages. `docs/examples/index.md` links to the notebook. `docs/maintainers/production-readiness.md` and `CONTRIBUTING.md` describe administration and release procedures. `.github/workflows/docs.yml` builds docs on pushes and deploys on dispatch through the `github-pages` environment. `pypi.yml` uses OpenID Connect (OIDC), GitHub's short-lived identity assertion, to publish only after validation and explicit publication selection. PyPI must separately trust the new repository owner.

## Plan of Work


First commit this plan and open a PR. Update active repository/Pages links to the new organization, add an explicit Documentation package URL, and update the current administrative handoff with concrete PyPI publisher fields and Pages deployment commands. Keep historical plan evidence intact. Inspect all tracked files for other owner-dependent integrations; change workflows only if an actual transfer dependency is found.

Then build docs and inspect rendered navigation, canonical URLs, nested pages and assets. Build the source archive and build its wheel, run the existing archive validator and inspect both archives' URL metadata. Run normal hooks and rely on the full hosted shared validation matrix for Python/runtime/checker/platform coverage. Merge only once required checks pass. Dispatch docs from the merged main and verify HTTP success, expected content, correct canonical URLs and reachable assets.

## Concrete Steps


Run in `/private/tmp/bearshape-ownership-transfer`:

    uv sync --locked
    uv run --locked prek install
    uv run --locked --only-group docs zensical build --clean
    uv run --locked --only-group docs python tools/check_docs.py
    uv build --sdist
    uv build dist/bearshape-0.1.0rc0.tar.gz --wheel
    uv run --locked python tools/check_distribution.py dist/*.whl dist/*.tar.gz
    uv run --locked prek run -a

Use `gh pr checks --repo beartype/bearshape` for the created PR. After green checks merge the exact reviewed head and run `gh workflow run docs.yml --repo beartype/bearshape --ref main`. Inspect the resulting run and fetch https://beartype.github.io/bearshape/ plus nested pages and referenced assets.

## Validation and Acceptance


The live home page, static typing guide, examples and logo must return HTTP 200. Canonical and sitemap URLs must use the new Pages origin, and repository/edit/notebook links must use `beartype/bearshape`. Both wheel and source archive metadata must contain the new repository, issues and documentation URLs. Normal hooks and the hosted required validation must pass. Record external settings that cannot be verified rather than claim successful future package publication.

## Idempotence and Recovery


Use the existing Pages site and environment. Dispatch can be repeated safely. Corrective commits can revert these focused link/documentation edits. Do not recreate a repository at the old owner/name because that would replace GitHub's repository redirect. Preserve other open PRs and worktrees. Only remove this worktree after the merged head is reachable from main and all evidence is committed.

## Artifacts and Notes


Local validation used uv 0.11.15 with the locked environment; hosted workflows pin uv 0.11.17. Zensical built cleanly; `check_docs.py` verified rendered tables, admonitions, favicon and 93 Python 3.10 snippets. Separate archive/render inspection verified 23 pages' canonical/repository URLs, 23 sitemap URLs, and all four Project-URL fields in both archives. The copied `site/overrides/main.html` is a template asset, not a generated documentation page. Browser inspection confirmed the homepage layout and new repository identity. Normal hooks pass after wrapping the longer release command.

The validated local wheel SHA256 is `0922f70b0fa9c79236b044bef430e85f89715dfdde586cccb0de169f3b5695c4`; source archive SHA256 is `025ded7e59d1ba17ef2bc3bd7bfbf524e1c157cd66809d6f9a0c1b1d0c3f1495`. These are repair validation artifacts, not a publication or fresh GPU validation claim.

Initial restoration workflow: https://github.com/beartype/bearshape/actions/runs/34451065635. Base main: `795ec39`. New repository homepage already matches https://beartype.github.io/bearshape/.

## Interfaces and Dependencies


Keep Zensical, locked uv, the existing artifact/Pages actions, GitHub Pages and PyPI OIDC. No runtime function signatures or dependencies change. PyPI trust must identify owner `beartype`, repository `bearshape`, workflow `pypi.yml`, environment `pypi`; no upload token is introduced.

Revision note — 2026-09-10: Initial plan records verified transfer, restoration dispatch and the user's repair/deployment authorization.

Revision note — 2026-09-10: Recorded PR #36, successful initial restoration, completed link/metadata edits, external PyPI limits and local validation evidence before final hosted validation and merge.
