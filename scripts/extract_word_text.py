#!/usr/bin/env python3
"""Extract readable text from Word Open XML resumes (.docx/.docm).

This script uses only the Python standard library so the skill can parse common
Word resumes without depending on python-docx.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TEXT_TAGS = {
    WORD_NS + "t",
    WORD_NS + "instrText",
}
BREAK_TAG = WORD_NS + "br"
TAB_TAG = WORD_NS + "tab"
PARA_TAG = WORD_NS + "p"
TABLE_ROW_TAG = WORD_NS + "tr"
TABLE_CELL_TAG = WORD_NS + "tc"


DOCUMENT_PARTS = [
    "word/document.xml",
    "word/footnotes.xml",
    "word/endnotes.xml",
    "word/comments.xml",
]


def iter_header_footer_parts(names: list[str]) -> list[str]:
    return sorted(
        name
        for name in names
        if name.startswith("word/header") or name.startswith("word/footer")
    )


def node_text(node: ET.Element) -> str:
    chunks: list[str] = []
    for child in node.iter():
        if child.tag in TEXT_TAGS and child.text:
            chunks.append(child.text)
        elif child.tag == TAB_TAG:
            chunks.append("\t")
        elif child.tag == BREAK_TAG:
            chunks.append("\n")
    return "".join(chunks).strip()


def extract_table(table_node: ET.Element) -> list[str]:
    rows: list[str] = []
    for row in table_node.iter(TABLE_ROW_TAG):
        cells = [node_text(cell) for cell in row.findall(".//" + TABLE_CELL_TAG)]
        cells = [cell for cell in cells if cell]
        if cells:
            rows.append(" | ".join(cells))
    return rows


def extract_xml_part(data: bytes) -> list[str]:
    root = ET.fromstring(data)
    blocks: list[str] = []

    def walk(node: ET.Element) -> None:
        for child in list(node):
            if child.tag == TABLE_ROW_TAG:
                row_cells = [node_text(cell) for cell in child.findall(".//" + TABLE_CELL_TAG)]
                row_cells = [cell for cell in row_cells if cell]
                if row_cells:
                    blocks.append(" | ".join(row_cells))
            elif child.tag == PARA_TAG:
                text = node_text(child)
                if text:
                    blocks.append(text)
            elif child.tag == WORD_NS + "tbl":
                walk(child)
            else:
                walk(child)

    walk(root)

    return blocks


def extract_word_text(path: Path) -> str:
    if path.suffix.lower() not in {".docx", ".docm"}:
        raise ValueError(
            "Only .docx/.docm are supported directly. Convert legacy .doc to .docx or PDF first."
        )

    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        parts = [part for part in DOCUMENT_PARTS if part in names]
        parts.extend(iter_header_footer_parts(names))

        sections: list[str] = []
        for part in parts:
            try:
                blocks = extract_xml_part(zf.read(part))
            except ET.ParseError:
                continue
            if blocks:
                label = part.removeprefix("word/").removesuffix(".xml")
                sections.append(f"## {label}\n" + "\n".join(blocks))

    return "\n\n".join(sections).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from .docx/.docm files.")
    parser.add_argument("path", help="Path to a Word .docx or .docm file")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    try:
        text = extract_word_text(path)
    except (ValueError, zipfile.BadZipFile) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not text:
        print("No readable text found. The document may be image-based or protected.", file=sys.stderr)
        return 1

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
