"""Publication identity checks against real disposable Git histories."""

# Synthetic repositories only; commands use argument lists, never a shell.

from __future__ import annotations

import json
import os
import runpy
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import TypeAlias

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "tools/check_release.py"
resolve_release = runpy.run_path(str(_SCRIPT))["resolve_release"]
Repository: TypeAlias = tuple[Path, Callable[..., str]]


@pytest.fixture
def repository(tmp_path: Path) -> Repository:
  git = shutil.which("git")
  assert git is not None

  def command(*args: str) -> str:
    return subprocess.check_output(
      [
        git,
        "-c",
        "user.name=Release test",
        "-c",
        "user.email=release@example.invalid",
        *args,
      ],
      cwd=tmp_path,
      text=True,
      stderr=subprocess.PIPE,
    ).strip()

  command("init", "-b", "main")
  (tmp_path / "content").write_text("first\n")
  command("add", "content")
  command("commit", "-m", "Initial synthetic release")
  command("update-ref", "refs/remotes/origin/main", "HEAD")
  command("tag", "v0.1.0rc0")
  return tmp_path, command


def resolve(repository: Repository, **overrides: object) -> dict[str, str]:
  root, git = repository
  options = {
    "repository": root,
    "version": "0.1.0rc0",
    "requested_ref": "v0.1.0rc0",
    "event_name": "workflow_dispatch",
    "workflow_ref": "refs/tags/v0.1.0rc0",
    "workflow_sha": git("rev-parse", "HEAD"),
    "event": {},
    "publish": True,
  }
  options.update(overrides)
  return resolve_release(**options)


def published_event(version: str, *, prerelease: bool, draft: bool = False) -> dict:
  return {
    "action": "published",
    "release": {"tag_name": f"v{version}", "prerelease": prerelease, "draft": draft},
  }


def test_candidate_tag_resolves_to_immutable_commit(repository: Repository) -> None:
  _, git = repository
  assert resolve(repository) == {
    "sha": git("rev-parse", "HEAD"),
    "version": "0.1.0rc0",
    "publish": "true",
  }


@pytest.mark.parametrize("version,prerelease", [("0.1.0rc0", True), ("0.1.0", False)])
def test_release_event_requires_matching_prerelease_status(
  repository: Repository, version: str, prerelease: bool
) -> None:
  _, git = repository
  git("tag", "-f", f"v{version}")
  assert (
    resolve(
      repository,
      version=version,
      requested_ref=f"v{version}",
      workflow_ref=f"refs/tags/v{version}",
      event_name="release",
      event=published_event(version, prerelease=prerelease),
      publish=False,
    )["publish"]
    == "true"
  )
  with pytest.raises(ValueError, match="prerelease status"):
    resolve(
      repository,
      version=version,
      requested_ref=f"v{version}",
      workflow_ref=f"refs/tags/v{version}",
      event_name="release",
      event=published_event(version, prerelease=not prerelease),
    )


@pytest.mark.parametrize(
  "ref", ["main", "refs/heads/main", "v0.1.0", "v0.1.0rc1", "v0.1.0rc0\nevil"]
)
def test_arbitrary_ref_cannot_publish(repository: Repository, ref: str) -> None:
  with pytest.raises(ValueError, match="exact version tag"):
    resolve(repository, requested_ref=ref)


@pytest.mark.parametrize(
  "version", ["01.1.0", "0.1.0+local", "0.1.0.dev0", "0.1.0.post1"]
)
def test_non_release_version_is_rejected(repository: Repository, version: str) -> None:
  with pytest.raises(ValueError, match="Release version"):
    resolve(repository, version=version, requested_ref=f"v{version}")


def test_missing_tag_is_rejected(repository: Repository) -> None:
  with pytest.raises(subprocess.CalledProcessError):
    resolve(
      repository,
      version="0.1.0rc1",
      requested_ref="v0.1.0rc1",
      workflow_ref="refs/tags/v0.1.0rc1",
    )


def test_tag_must_identify_checked_out_commit(repository: Repository) -> None:
  root, git = repository
  (root / "content").write_text("second\n")
  git("commit", "-am", "Another synthetic commit")
  git("update-ref", "refs/remotes/origin/main", "HEAD")
  with pytest.raises(ValueError, match="checked-out commit"):
    resolve(repository)


def test_release_commit_must_already_be_on_main(repository: Repository) -> None:
  root, git = repository
  (root / "content").write_text("unmerged\n")
  git("commit", "-am", "Unmerged synthetic candidate")
  git("tag", "v0.1.0rc1")
  with pytest.raises(ValueError, match="main history"):
    resolve(
      repository,
      version="0.1.0rc1",
      requested_ref="v0.1.0rc1",
      workflow_ref="refs/tags/v0.1.0rc1",
    )


def test_draft_release_cannot_publish(repository: Repository) -> None:
  with pytest.raises(ValueError, match="non-draft"):
    resolve(
      repository,
      event_name="release",
      event=published_event("0.1.0rc0", prerelease=True, draft=True),
    )


def test_validation_only_dispatch_emits_nonpublishing_identity(
  repository: Repository,
) -> None:
  root, git = repository
  event_path, output_path = root / "event.json", root / "output.txt"
  event_path.write_text("{}")
  environment = dict(
    os.environ,
    GITHUB_EVENT_PATH=str(event_path),
    GITHUB_EVENT_NAME="workflow_dispatch",
    GITHUB_REF="refs/heads/main",
    GITHUB_WORKFLOW_SHA=git("rev-parse", "HEAD"),
    GITHUB_OUTPUT=str(output_path),
    PROJECT_VERSION="0.1.0rc0",
    RELEASE_REF="main",
    PUBLISH="false",
  )
  result = subprocess.run(
    [sys.executable, str(_SCRIPT)],
    cwd=root,
    env=environment,
    check=True,
    capture_output=True,
    text=True,
  )
  assert json.loads(result.stdout) == {
    "sha": git("rev-parse", "HEAD"),
    "version": "0.1.0rc0",
    "publish": "false",
  }
  assert "publish=false\n" in output_path.read_text()


@pytest.mark.parametrize(
  "override",
  [{"workflow_ref": "refs/heads/main"}, {"workflow_sha": "0" * 40}],
)
def test_publication_workflow_must_match_candidate(
  repository: Repository, override: dict[str, str]
) -> None:
  with pytest.raises(ValueError, match="matching version tag and commit"):
    resolve(repository, **override)
