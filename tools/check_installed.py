"""Normally install a candidate wheel and test consumers outside the checkout."""

# Command driver: argument lists only, never a shell.
# ruff: noqa: S404, S603

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from check_distribution import check_distribution

_CONFIGS = {"pyproject.toml", "pytest.toml", "ty.toml", "uv.lock"}
_ORIGIN_CHECK = """
import importlib.metadata
import json
import pathlib
import sys
import bearshape
import beartype
origin = pathlib.Path(bearshape.__file__).resolve()
assert origin.is_relative_to(pathlib.Path(sys.prefix)), origin
assert beartype.__version__ == '0.23.0rc0', beartype.__version__
metadata = importlib.metadata.distribution('bearshape')
direct = json.loads(metadata.read_text('direct_url.json') or '{}')
assert not direct.get('dir_info', {}).get('editable'), direct
print(json.dumps({'python': sys.version, 'bearshape': bearshape.__version__,
                  'beartype': beartype.__version__, 'module': str(origin)}, indent=2))
"""


def _copy_consumers(sdist: Path, destination: Path) -> None:
  prefix = sdist.name.removesuffix(".tar.gz") + "/"
  with tarfile.open(sdist, "r:gz") as archive:
    for member in archive.getmembers():
      name = member.name.removeprefix(prefix)
      if not member.isfile() or not (
        name.startswith("tests/")
        or name in _CONFIGS
        or name == "tools/validate_runtime.py"
      ):
        continue
      target = (destination / name).resolve()
      if not target.is_relative_to(destination):
        message = f"Invalid consumer archive path: {member.name}"
        raise ValueError(message)
      stream = archive.extractfile(member)
      if stream is None:
        message = f"Cannot read consumer file: {member.name}"
        raise ValueError(message)
      target.parent.mkdir(parents=True, exist_ok=True)
      target.write_bytes(stream.read())


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("wheel", type=Path)
  parser.add_argument("sdist", type=Path)
  parser.add_argument("--python", required=True, help="Consumer Python version")
  args = parser.parse_args()
  uv = shutil.which("uv")
  if uv is None:
    parser.error("uv is required to create the isolated consumer environment")
  wheel, sdist = args.wheel.resolve(), args.sdist.resolve()
  evidence = check_distribution(wheel, sdist)
  json.dump(evidence, sys.stdout, indent=2)
  sys.stdout.write("\n")
  sys.stdout.flush()
  environment = dict(os.environ, UV_TORCH_BACKEND="cpu")
  for key in ("PYTHONPATH", "PYTHONHOME", "TOX_ENV_NAME"):
    environment.pop(key, None)

  with tempfile.TemporaryDirectory(prefix="bearshape-installed-") as temporary:
    consumer = Path(temporary).resolve()
    _copy_consumers(sdist, consumer)
    requirements = consumer / "requirements.txt"
    subprocess.run(
      [
        uv,
        "export",
        "--locked",
        "--no-default-groups",
        "--group",
        "optional",
        "--group",
        "static",
        "--group",
        "test",
        "--no-emit-project",
        "--output-file",
        str(requirements),
      ],
      check=True,
      cwd=consumer,
      env=environment,
      stdout=subprocess.DEVNULL,
    )
    venv = consumer / ".venv"
    subprocess.run(
      [uv, "venv", "--python", args.python, str(venv)],
      check=True,
      cwd=consumer,
      env=environment,
    )
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(
      [uv, "pip", "sync", "--python", str(python), str(requirements)],
      check=True,
      cwd=consumer,
      env=environment,
    )
    subprocess.run(
      [
        uv,
        "pip",
        "install",
        "--python",
        str(python),
        str(wheel),
        "beartype==0.23.0rc0",
      ],
      check=True,
      cwd=consumer,
      env=environment,
    )
    subprocess.run(
      [str(python), "-I", "-c", _ORIGIN_CHECK],
      check=True,
      cwd=consumer,
      env=environment,
    )
    subprocess.run(
      [str(python), "-I", "tools/validate_runtime.py", "cpu"],
      check=True,
      cwd=consumer,
      env=environment,
    )
    subprocess.run(
      [str(python), "-I", "-m", "pytest", "tests/", "--installed-package", "-n", "4"],
      check=True,
      cwd=consumer,
      env=environment,
    )


if __name__ == "__main__":
  main()
