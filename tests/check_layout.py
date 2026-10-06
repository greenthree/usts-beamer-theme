"""Check Beamer layout and compare the USTS theme with a Madrid baseline."""

import argparse
import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command, cwd=ROOT, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True)
    if result.returncode:
        raise RuntimeError(
            f"Command failed: {command}\n"
            + (result.stdout + result.stderr).decode("utf-8", errors="replace")
        )
    return result.stdout


def compile_pdf(source, name, build_dir, cwd, args):
    output = build_dir / name
    output.mkdir(parents=True, exist_ok=True)
    tex = output / f"{name}.tex"
    tex.write_text(source, encoding="utf-8")
    env = os.environ.copy()
    # Relative paths also avoid Windows TeX's non-ASCII environment-path issue.
    theme_path = Path(os.path.relpath(ROOT, cwd)).as_posix()
    env["TEXINPUTS"] = theme_path + os.pathsep + env.get("TEXINPUTS", "")
    run(
        [
            args.latexmk,
            "-xelatex",
            "-quiet",
            "-g",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={output.as_posix()}",
            tex.as_posix(),
        ],
        cwd=cwd,
        env=env,
    )
    return tex.with_suffix(".pdf")


def pdf_pages(pdf, args):
    xml = run([args.pdftotext, "-bbox-layout", str(pdf), "-"])
    return ET.fromstring(xml).findall(".//{*}page")


def page_text(page, footer=False):
    words = page.findall(".//{*}word")
    if footer:
        bottom = float(page.get("height")) - 12
        words = [word for word in words if float(word.get("yMin")) > bottom]
    return "".join(word.text or "" for word in words).replace(" ", "")


def check_fixture(pages, wide):
    assert len(pages) == 11, f"Expected 11 fixture pages, got {len(pages)}"
    expected_ratio = 16 / 9 if wide else 4 / 3
    for number, page in enumerate(pages, 1):
        width, height = float(page.get("width")), float(page.get("height"))
        assert abs(width / height - expected_ratio) < 0.001, "Wrong slide aspect ratio"
        for word in page.findall(".//{*}word"):
            x0, y0, x1, y1 = (
                float(word.get(key)) for key in ("xMin", "yMin", "xMax", "yMax")
            )
            assert -0.5 <= x0 <= x1 <= width + 0.5, f"Page {number}: text outside width: {word.text}"
            assert -0.5 <= y0 <= y1 <= height + 0.5, f"Page {number}: text outside height: {word.text}"
    assert "（苏州科技大学ACM集训队）" in page_text(pages[0]), "Cover institute is missing"
    assert "(USTSACM)" in page_text(pages[0], footer=True), "Short institute is missing"
    assert "手动换行第一行" in page_text(pages[3])
    assert "手动换行第二行" in page_text(pages[3])
    assert "自动换行标题开头" in page_text(pages[4])
    assert "自动换行标题结尾" in page_text(pages[4])
    assert "副标题内容" in page_text(pages[5])
    for index in (6, 7):
        footer = page_text(pages[index], footer=True)
        assert "绿化三" in footer and "(" not in footer, "Empty institute produced parentheses"
    assert "苏州科技大学" in page_text(pages[8], footer=True)
    assert "(USTS)" in page_text(pages[9], footer=True)
    assert "10/10" in page_text(pages[9], footer=True), "Frame count did not converge"
    assert page_text(pages[10], footer=True) == "", "plain frame still has a footer"


def compare(baseline, actual, args):
    baseline_pages, actual_pages = pdf_pages(baseline, args), pdf_pages(actual, args)
    assert len(baseline_pages) == len(actual_pages), "Baseline/USTS page counts differ"
    for number, (expected, page) in enumerate(zip(baseline_pages, actual_pages), 1):
        assert expected.get("width") == page.get("width"), f"Page {number}: width differs"
        assert expected.get("height") == page.get("height"), f"Page {number}: height differs"
        images = []
        for pdf in (baseline, actual):
            # With no output prefix, Poppler returns a PPM image on stdout.
            images.append(
                run([
                    args.pdftoppm, "-r", "144", "-f", str(number),
                    "-l", str(number), "-singlefile", str(pdf),
                ])
            )
        assert images[0].startswith(b"P6"), "Poppler did not return a PPM image"
        assert images[0] == images[1], f"Page {number}: pixel mismatch ({baseline.name}, {actual.name})"
    print(f"{actual.stem}: {len(actual_pages)} pages pixel-identical at 144 dpi", flush=True)
    return actual_pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, default=ROOT / "build" / "layout")
    parser.add_argument("--latexmk", default="latexmk")
    parser.add_argument("--pdftoppm", default="pdftoppm")
    parser.add_argument("--pdftotext", default="pdftotext")
    args = parser.parse_args()
    build_dir = args.build_dir.resolve()
    for wide in (False, True):
        ratio = "169" if wide else "43"
        prefix = "\\def\\USTSWide{1}\n" if wide else ""
        fixture = prefix + "\\input{tests/regression.tex}\n"
        baseline = compile_pdf(
            "\\def\\USTSBaseline{1}\n" + fixture,
            f"baseline-{ratio}", build_dir, ROOT, args,
        )
        actual = compile_pdf(fixture, f"usts-{ratio}", build_dir, ROOT, args)
        check_fixture(compare(baseline, actual, args), wide)
    print("All layout checks passed.", flush=True)


if __name__ == "__main__":
    main()
