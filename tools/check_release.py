"""Resolve release identity before allowing artifact validation or publication."""

# Git commands use argument lists and never a shell.
# ruff: noqa: S404, S603

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

_VERSION = re.compile(
  r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:(a|b|rc)(0|[1-9]\d*))?"
)


def git_environment(git: str) -> dict[str, str]:
  """Clear hook-local Git variables before addressing an explicit repository."""
  local_names = subprocess.check_output(
    [git, "rev-parse", "--local-env-vars"], text=True
  ).splitlines()
  return {key: value for key, value in os.environ.items() if key not in local_names}


def resolve_release(
  *,
  repository: Path,
  version: str,
  requested_ref: str,
  event_name: str,
  workflow_ref: str,
  workflow_sha: str,
  event: dict,
  publish: bool,
) -> dict[str, str]:
  """Reject publication unless version, tag, ancestry and event agree."""
  match = _VERSION.fullmatch(version)
  if match is None:
    message = f"Release version must be X.Y.Z with an optional a/b/rc suffix: {version}"
    raise ValueError(message)
  if event_name not in {"release", "workflow_dispatch"}:
    message = f"Unsupported release event: {event_name}"
    raise ValueError(message)
  git = shutil.which("git")
  if git is None:
    message = "git is required to resolve the release commit"
    raise RuntimeError(message)

  environment = git_environment(git)

  def revision(ref: str) -> str:
    return subprocess.check_output(
      [git, "rev-parse", "--verify", ref], cwd=repository, env=environment, text=True
    ).strip()

  commit = revision("HEAD^{commit}")
  if event_name == "release":
    release = event["release"]
    if event["action"] != "published" or release["draft"]:
      message = "Only a published, non-draft GitHub release can publish"
      raise ValueError(message)
    if requested_ref != release["tag_name"]:
      message = "Requested ref differs from the published release tag"
      raise ValueError(message)
    if release["prerelease"] != (match.group(4) is not None):
      message = "GitHub prerelease status differs from the package version"
      raise ValueError(message)
    publish = True

  if publish:
    if requested_ref != f"v{version}":
      message = f"Publication requires the exact version tag v{version}"
      raise ValueError(message)
    if workflow_ref != f"refs/tags/{requested_ref}" or workflow_sha != commit:
      message = "Publication workflow must run from the matching version tag and commit"
      raise ValueError(message)
    if revision(f"refs/tags/{requested_ref}^{{commit}}") != commit:
      message = "Release tag does not identify the checked-out commit"
      raise ValueError(message)
    ancestry = subprocess.run(
      [git, "merge-base", "--is-ancestor", commit, "refs/remotes/origin/main"],
      cwd=repository,
      env=environment,
      check=False,
    )
    if ancestry.returncode == 1:
      message = "Release commit must already belong to origin/main history"
      raise ValueError(message)
    ancestry.check_returncode()
  return {"sha": commit, "version": version, "publish": str(publish).lower()}


def main() -> None:
  event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
  result = resolve_release(
    repository=Path.cwd(),
    version=os.environ["PROJECT_VERSION"],
    requested_ref=os.environ["RELEASE_REF"],
    event_name=os.environ["GITHUB_EVENT_NAME"],
    workflow_ref=os.environ["GITHUB_REF"],
    workflow_sha=os.environ["GITHUB_WORKFLOW_SHA"],
    event=event,
    publish=os.environ["PUBLISH"] == "true",
  )
  sys.stdout.write(json.dumps(result, indent=2) + "\n")
  with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
    output.writelines(f"{name}={value}\n" for name, value in result.items())


if __name__ == "__main__":
  main()
