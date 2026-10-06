"""Check text presence and geometry in the Beamer regression PDFs."""

import argparse
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def text(words):
    return "".join(word.text or "" for word in words).replace(" ", "")


def check_pdf(path, pdftotext):
    result = subprocess.run(
        [pdftotext, "-bbox-layout", str(path), "-"],
        check=True,
        capture_output=True,
    )
    pages = ET.fromstring(result.stdout).findall(".//{*}page")
    assert len(pages) == 11, f"{path}: expected 11 pages, got {len(pages)}"

    footers = []
    headers = []
    for number, page in enumerate(pages, 1):
        width, height = float(page.get("width")), float(page.get("height"))
        words = page.findall(".//{*}word")
        for word in words:
            x0, y0, x1, y1 = (float(word.get(key)) for key in ("xMin", "yMin", "xMax", "yMax"))
            assert -0.5 <= x0 <= x1 <= width + 0.5, f"{path}: page {number}: text outside page: {word.text}"
            assert -0.5 <= y0 <= y1 <= height + 0.5, f"{path}: page {number}: text outside page: {word.text}"

        header = [word for word in words if float(word.get("yMax")) < height * 0.35]
        footer = [word for word in words if float(word.get("yMin")) > height - 14]
        headers.append(text(header))
        footers.append(text(footer))
        if number in (1, 2):
            assert "Author" in text(footer) and "(" not in text(footer), f"{path}: empty institute produced parentheses"

        # The fixture uses 0.65 cm text margins (PDF coordinates are in points).
        margin = 0.65 * 72 / 2.54
        for word in footer:
            assert float(word.get("xMax")) <= width - margin + 0.5, f"{path}: page {number}: missing right footer margin"
            if number == 9:
                assert float(word.get("xMin")) >= margin - 0.5, f"{path}: missing left minimal-footer margin"

        # Page 9 uses the minimal footer; page 10 has no footer.
        boundaries = [0, 0.84 * width, width] if number == 9 else [0, 0.32 * width, 0.68 * width, width]
        for word in footer:
            x0, x1 = float(word.get("xMin")), float(word.get("xMax"))
            center = (x0 + x1) / 2
            column = next(index for index in range(len(boundaries) - 1) if center <= boundaries[index + 1])
            assert x0 >= boundaries[column] - 0.5 and x1 <= boundaries[column + 1] + 0.5, (
                f"{path}: page {number}: footer crosses a column: {word.text}"
            )

    assert "苏州科技大学" in footers[2], f"{path}: full institute missing from footer"
    assert "(USTS)" in footers[3], f"{path}: short institute missing from footer"
    assert "自动换行标题开头" in headers[4] and "自动换行标题结尾" in headers[4], f"{path}: automatic title wrap clipped"
    assert "手动换行第一行" in headers[5] and "手动换行第二行" in headers[5], f"{path}: explicit title line clipped"
    assert "主标题" in headers[6] and "副标题内容" in headers[6], f"{path}: subtitle missing"
    assert "FirstAuthor" in footers[7] and "FourthAuthor" in footers[7], f"{path}: author list truncated"
    for index in (7, 8):
        assert "Averylongreporttitle" in footers[index] and "conclusions" in footers[index], f"{path}: long footer title truncated"
    assert "October6,2026" in footers[7], f"{path}: long date truncated"
    assert footers[9] == "", f"{path}: none mode still shows a footer"
    assert "Team(USTS)" in footers[10] and "Short" in footers[10], f"{path}: short metadata missing"
    print(f"{path.name}: 11 pages passed title and footer checks")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="+", type=Path)
    parser.add_argument("--pdftotext", default="pdftotext", help="Path to the Poppler executable")
    args = parser.parse_args()
    for pdf in args.pdfs:
        check_pdf(pdf, args.pdftotext)
