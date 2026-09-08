"""Verify the wheel and source archive that will be released.

Usage: python tools/check_distribution.py package.whl package.tar.gz
"""

from __future__ import annotations

import hashlib
import json
import sys
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

SOURCE_INPUTS = {
  "LICENSE",
  "README.md",
  "CHANGELOG.md",
  "CONTRIBUTING.md",
  "pyproject.toml",
  "uv.lock",
  "pytest.toml",
  "tox.toml",
  "ty.toml",
  "ruff.toml",
  "tools/check_distribution.py",
  "tools/check_installed.py",
  "tools/check_release.py",
  "tools/validate_runtime.py",
  "tools/validate_tox_env.py",
  "tests/conftest.py",
  "tests/test_numpy.py",
  "tests/test_tree.py",
  "tests/test_typecheck.py",
  "tests/typing/check_imports.py",
  "tests/typing_negative/invalid_calls.py",
}


def _read_source(sdist: Path, prefix: str) -> dict[str, bytes]:
  source_files: dict[str, bytes] = {}
  with tarfile.open(sdist, "r:gz") as archive:
    for member in archive.getmembers():
      if not member.isfile():
        continue
      if not member.name.startswith(prefix):
        msg = f"Source archive member has the wrong release prefix: {member.name}"
        raise ValueError(msg)
      stream = archive.extractfile(member)
      if stream is None:
        msg = f"Cannot read source archive member: {member.name}"
        raise ValueError(msg)
      source_files[member.name.removeprefix(prefix)] = stream.read()
  return source_files


def check_distribution(wheel: Path, sdist: Path) -> dict[str, str]:
  with zipfile.ZipFile(wheel) as archive:
    wheel_files = {
      name: archive.read(name) for name in archive.namelist() if not name.endswith("/")
    }
  metadata_paths = [
    name for name in wheel_files if name.endswith(".dist-info/METADATA")
  ]
  if len(metadata_paths) != 1:
    msg = "Wheel must contain exactly one distribution metadata file"
    raise ValueError(msg)
  metadata_path = metadata_paths[0]
  metadata = BytesParser().parsebytes(wheel_files[metadata_path])
  if metadata["Name"] != "bearshape" or metadata["License-Expression"] != "MIT":
    msg = "Wheel must declare bearshape and the MIT license expression"
    raise ValueError(msg)
  if metadata.get_all("License-File") != ["LICENSE"]:
    msg = "Wheel metadata must declare License-File: LICENSE"
    raise ValueError(msg)
  license_path = metadata_path.removesuffix("METADATA") + "licenses/LICENSE"
  license_text = (Path(__file__).resolve().parents[1] / "LICENSE").read_bytes()
  if wheel_files.get(license_path) != license_text:
    msg = "Wheel must contain the complete repository LICENSE text"
    raise ValueError(msg)
  version = metadata["Version"]
  if not version:
    msg = "Wheel must declare a version"
    raise ValueError(msg)
  prefix = f"bearshape-{version}/"
  source_files = _read_source(sdist, prefix)
  if missing := SOURCE_INPUTS - source_files.keys():
    msg = f"Source archive is missing downstream inputs: {sorted(missing)}"
    raise ValueError(msg)
  source_metadata = BytesParser().parsebytes(source_files["PKG-INFO"])
  for field in (
    "Name",
    "Version",
    "License-Expression",
    "License-File",
    "Requires-Python",
    "Requires-Dist",
  ):
    if source_metadata.get_all(field) != metadata.get_all(field):
      msg = f"Wheel and source metadata disagree on {field}"
      raise ValueError(msg)
  if source_files["LICENSE"] != license_text:
    msg = "Source archive must contain the complete repository LICENSE text"
    raise ValueError(msg)
  wheel_package = {
    name: content
    for name, content in wheel_files.items()
    if name.startswith("bearshape/")
  }
  source_package = {
    name.removeprefix("src/"): content
    for name, content in source_files.items()
    if name.startswith("src/bearshape/")
  }
  if not wheel_package or "bearshape/py.typed" not in wheel_package:
    msg = "Wheel must contain the package and its py.typed marker"
    raise ValueError(msg)
  if wheel_package != source_package:
    msg = "Wheel package contents differ from the source archive"
    raise ValueError(msg)
  for name in (*wheel_files, *source_files):
    if any(
      part in {"__pycache__", ".venv", ".tox", ".git", "site"}
      for part in Path(name).parts
    ) or name.endswith((".pyc", ".pyo")):
      msg = f"Distribution contains a generated or private file: {name}"
      raise ValueError(msg)
  return {
    "version": version,
    "wheel": wheel.name,
    "wheel_sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
    "sdist": sdist.name,
    "sdist_sha256": hashlib.sha256(sdist.read_bytes()).hexdigest(),
  }


def main() -> None:
  if len(sys.argv) != 3:
    sys.exit("usage: check_distribution.py package.whl package.tar.gz")
  json.dump(
    check_distribution(Path(sys.argv[1]), Path(sys.argv[2])), sys.stdout, indent=2
  )
  sys.stdout.write("\n")


if __name__ == "__main__":
  main()
