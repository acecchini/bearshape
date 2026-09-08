"""Fail early when a required candidate backend is missing or incorrectly built."""

from __future__ import annotations

import argparse
import importlib
import json
import sys

_BACKENDS = ("numpy", "jax", "torch", "optree")


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("environment", nargs="?", default="cpu")
  args = parser.parse_args()
  factors = args.environment.split("-")
  if any(factor in {"cpu", "dev", "type"} for factor in factors):
    backends = _BACKENDS
  else:
    backends = tuple(
      name for name in _BACKENDS if any(f.startswith(name) for f in factors)
    )
  if not backends:
    parser.error(f"no expected backend in {args.environment!r}")

  versions = {}
  for name in ("bearshape", "beartype", *backends):
    module = importlib.import_module(name)
    versions[name] = {
      "version": module.__version__,
      "path": module.__file__,
    }
    if name == "beartype" and module.__version__ != "0.23.0rc0":
      message = f"expected beartype 0.23.0rc0, found {module.__version__}"
      raise SystemExit(message)
    if name == "torch" and (
      module.version.cuda is not None or module.version.hip is not None
    ):
      message = "CPU validation requires a CPU-only Torch build"
      raise SystemExit(message)
  sys.stdout.write(
    json.dumps({"python": sys.version, "modules": versions}, indent=2) + "\n"
  )


if __name__ == "__main__":
  main()
