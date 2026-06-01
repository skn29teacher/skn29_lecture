"""Convert a Jupyter notebook (.ipynb) to a Python script (.py).

The exporter preserves notebook structure with VS Code / Jupyter cell markers:

- Code cells become plain Python blocks prefixed with ``# %%``
- Markdown cells become commented sections prefixed with ``# %% [markdown]``

Usage:

    python convert_notebook_to_py.py input.ipynb
    python convert_notebook_to_py.py input.ipynb output.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def _normalize_source(source: object) -> str:
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    if source is None:
        return ""
    return str(source)


def _comment_block(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines:
        return ["#"]
    commented: list[str] = []
    for line in lines:
        if line.strip():
            commented.append(f"# {line}")
        else:
            commented.append("#")
    return commented


def notebook_to_python(notebook_path: Path) -> str:
    data = json.loads(notebook_path.read_text(encoding="utf-8"))
    cells = data.get("cells", [])

    future_imports: list[str] = []
    for cell in cells:
        if cell.get("cell_type", "") != "code":
            continue
        source = _normalize_source(cell.get("source", ""))
        for line in source.splitlines():
            if line.startswith("from __future__ import ") and line not in future_imports:
                future_imports.append(line)

    output_lines: list[str] = []
    future_block_emitted = False
    for cell in cells:
        cell_type = cell.get("cell_type", "")
        source = _normalize_source(cell.get("source", ""))

        if cell_type == "markdown":
            output_lines.append("# %% [markdown]")
            output_lines.extend(_comment_block(source.rstrip("\n")))
        elif cell_type == "code":
            code_lines = [
                line
                for line in source.rstrip("\n").splitlines()
                if not line.startswith("from __future__ import ")
            ]

            if future_imports and not future_block_emitted:
                output_lines.append("# %%")
                output_lines.extend(future_imports)
                output_lines.append("")
                future_block_emitted = True

            output_lines.append("# %%")
            output_lines.extend(code_lines)
        else:
            output_lines.append(f"# %% [unknown cell type: {cell_type}]")
            output_lines.extend(_comment_block(source.rstrip("\n")))

        output_lines.append("")

    return "\n".join(output_lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to the .ipynb file")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Optional output .py path. Defaults to the same name as the notebook.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    notebook_path: Path = args.input
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")
    if notebook_path.suffix.lower() != ".ipynb":
        raise ValueError(f"Input must be a .ipynb file: {notebook_path}")

    output_path: Path = args.output or notebook_path.with_suffix(".py")
    output_path.write_text(notebook_to_python(notebook_path), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())