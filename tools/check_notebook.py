"""Execute the tour in a fresh kernel from the selected Python environment."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
  notebook = nbformat.read(ROOT / "examples/bearshape_tour.ipynb", as_version=4)
  for cell in notebook.cells:
    if cell.cell_type == "code":
      cell.execution_count = None
      cell.outputs = []
  with tempfile.TemporaryDirectory(prefix="bearshape-notebook-") as temporary:
    kernel = Path(temporary) / "bearshape-tour"
    kernel.mkdir()
    (kernel / "kernel.json").write_text(
      json.dumps({
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "bearshape tour validation",
        "language": "python",
      })
    )
    manager = KernelManager(
      kernel_name="bearshape-tour",
      kernel_spec_manager=KernelSpecManager(kernel_dirs=[temporary]),
    )
    client = NotebookClient(
      notebook, km=manager, timeout=180, resources={"metadata": {"path": temporary}}
    )
    try:
      client.execute()
    finally:
      if manager.has_kernel:
        manager.shutdown_kernel(now=True)
  output = ROOT / "build/bearshape_tour-executed.ipynb"
  output.parent.mkdir(exist_ok=True)
  nbformat.write(notebook, output)
  count = sum(cell.cell_type == "code" for cell in notebook.cells)
  sys.stdout.write(f"Executed {count} notebook cells with {sys.executable}\n")


if __name__ == "__main__":
  main()
