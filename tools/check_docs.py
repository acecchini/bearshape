"""Check rendered documentation structures and the Python 3.10 example syntax."""

from __future__ import annotations

import ast
import re
import sys
import textwrap
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_ROWS = {
  "api/index": [8],
  "api/bearshape": [5, 3],
  "features/claw": [3],
  "features/dimensions": [10, 11],
  "features/like-types": [6],
  "features/static-typing": [7],
  "features/tree-annotations": [8],
  "getting-started/installation": [6],
}
ADMONITIONS = {
  "features/decorator": 2,
  "features/dimensions": 2,
  "features/like-types": 2,
  "getting-started/installation": 1,
  "getting-started/quickstart": 1,
}


class _Structures(HTMLParser):
  def __init__(self) -> None:
    super().__init__()
    self.rows: list[int] = []
    self.admonitions = 0

  def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
    if tag == "table":
      self.rows.append(0)
    elif tag == "tr":
      self.rows[-1] += 1
    if tag == "div" and "admonition" in (dict(attrs).get("class") or "").split():
      self.admonitions += 1


def main() -> None:
  snippets = 0
  for path in (ROOT / "docs").rglob("*.md"):
    for code in re.findall(r"```python\n(.*?)\n\s*```", path.read_text(), re.DOTALL):
      ast.parse(textwrap.dedent(code), filename=str(path), feature_version=(3, 10))
      snippets += 1
  for page in TABLE_ROWS.keys() | ADMONITIONS.keys():
    parsed = _Structures()
    directory = page.removesuffix("/index")
    parsed.feed((ROOT / "site" / directory / "index.html").read_text())
    if page in TABLE_ROWS and parsed.rows != TABLE_ROWS[page]:
      message = f"{page}: expected table rows {TABLE_ROWS[page]}, got {parsed.rows}"
      raise ValueError(message)
    if page in ADMONITIONS and parsed.admonitions != ADMONITIONS[page]:
      message = (
        f"{page}: expected {ADMONITIONS[page]} admonitions, got {parsed.admonitions}"
      )
      raise ValueError(message)
  if not (ROOT / "site/assets/logo.svg").is_file():
    message = "Rendered logo/favicon is missing"
    raise FileNotFoundError(message)
  sys.stdout.write(
    f"Verified rendered tables, admonitions, favicon and {snippets} Python 3.10 snippets\n"
  )


if __name__ == "__main__":
  main()
