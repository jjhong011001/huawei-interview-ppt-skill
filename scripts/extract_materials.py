#!/usr/bin/env python3
"""Extract line-numbered candidate claims from text, Markdown, or LaTeX."""

import argparse
import json
import re
from pathlib import Path


def extract(path: Path) -> list[dict[str, object]]:
    results = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("%"):
            continue
        if not (re.match(r"^(?:[#*-]|\\(?:item|section|subsection|cventry)\b)", line)
                or any(term in line for term in ("项目简介", "负责功能", "国家级", "Recall@", "专利", "Under Review"))):
            continue
        line = re.sub(r"\\(?:textbf|textit)\{([^{}]*)\}", r"\1", line)
        line = line.replace("\\%", "%").replace("\\&", "&")
        results.append({"source": str(path.resolve()), "line": number, "text": line})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    records = []
    for path in args.inputs:
        if path.suffix.lower() not in {".md", ".tex", ".txt"}:
            parser.error(f"Unsupported input: {path}")
        records.extend(extract(path))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} source excerpts to {args.output}")


if __name__ == "__main__":
    main()
