#!/usr/bin/env python3
"""Check a PPTX for slide count, notes, and unresolved placeholders."""

import argparse
import posixpath
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def resolve(owner: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target))


def slide_text(root: ET.Element) -> str:
    return " ".join(item.text or "" for item in root.iter(A + "t"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--min-slides", type=int, default=1)
    args = parser.parse_args()
    problems = []
    with ZipFile(args.pptx) as archive:
        bad = archive.testzip()
        if bad:
            problems.append(f"Damaged ZIP member: {bad}")
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        links = {
            item.get("Id"): item.get("Target")
            for item in ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
        }
        slide_ids = list(presentation.find(P + "sldIdLst"))
        if len(slide_ids) < args.min_slides:
            problems.append(f"Only {len(slide_ids)} slides")
        names = set(archive.namelist())
        for number, slide_id in enumerate(slide_ids, 1):
            slide = resolve("ppt/presentation.xml", links[slide_id.get(R + "id")])
            visible = slide_text(ET.fromstring(archive.read(slide)))
            if not visible.strip():
                problems.append(f"Slide {number} has no visible text")
            if re.search(r"\[\[.*?\]\]|TODO|TBD|待填写|请替换", visible, re.I):
                problems.append(f"Slide {number} contains an unresolved placeholder")
            rels_name = posixpath.join(posixpath.dirname(slide), "_rels", posixpath.basename(slide) + ".rels")
            if rels_name not in names:
                problems.append(f"Slide {number} has no speaker notes")
                continue
            rels = ET.fromstring(archive.read(rels_name))
            target = next((item.get("Target") for item in rels if item.get("Type", "").endswith("/notesSlide")), None)
            if not target:
                problems.append(f"Slide {number} has no speaker notes")
                continue
            note = resolve(slide, target)
            note_text = slide_text(ET.fromstring(archive.read(note)))
            if not note_text.strip() or note_text.strip() == str(number):
                problems.append(f"Slide {number} has empty speaker notes")
    if problems:
        for problem in problems:
            print(problem)
        raise SystemExit(1)
    print(f"Checked {len(slide_ids)} slides: notes present, no unresolved text placeholders.")


if __name__ == "__main__":
    main()
