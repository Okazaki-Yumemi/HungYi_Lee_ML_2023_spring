#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import gdown
import requests
from bs4 import BeautifulSoup


COURSE_PAGE = "https://speech.ee.ntu.edu.tw/~hylee/ml/2023-spring.php"

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_ROOT = ROOT / "resources"
RAW_ROOT = RESOURCE_ROOT / "raw"

LECTURE_PDF_DIR = RAW_ROOT / "lecture-pdfs"
HOMEWORK_PDF_DIR = RAW_ROOT / "homework-pdfs"
NOTEBOOK_DIR = RAW_ROOT / "notebooks"
CATALOG_PATH = RESOURCE_ROOT / "catalog.md"

for directory in (
    LECTURE_PDF_DIR,
    HOMEWORK_PDF_DIR,
    NOTEBOOK_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


session = requests.Session()
session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 Chrome/130 Safari/537.36"
        )
    }
)


def safe_filename(name: str) -> str:
    """Convert a URL or page label into a Linux-safe filename."""
    name = unquote(name).strip()
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)
    name = re.sub(r"\s+", " ", name)
    return name[:180] or "unnamed"


def url_hash(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def download_file(url: str, destination: Path) -> None:
    """Download atomically, skipping files already present."""
    if destination.exists() and destination.stat().st_size > 0:
        print(f"[skip] {relative(destination)}")
        return

    temporary = destination.with_suffix(destination.suffix + ".part")

    print(f"[download] {url}")
    with session.get(
        url,
        stream=True,
        timeout=(15, 180),
        allow_redirects=True,
    ) as response:
        response.raise_for_status()

        content_type = response.headers.get("content-type", "").lower()
        if destination.suffix.lower() == ".pdf" and "text/html" in content_type:
            raise RuntimeError(
                f"Expected PDF but received HTML from {url}"
            )

        with temporary.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    temporary.replace(destination)


def page_context(anchor) -> str:
    """Obtain a useful label, including the homework row when possible."""
    own_text = " ".join(anchor.stripped_strings).strip()
    if own_text:
        return own_text

    row = anchor.find_parent("tr")
    if row is not None:
        row_text = " ".join(row.stripped_strings).strip()
        if row_text:
            return row_text[:200]

    parent_text = " ".join(anchor.parent.stripped_strings).strip()
    return parent_text[:200] or "unlabelled link"


def infer_hw_number(text: str) -> int | None:
    match = re.search(r"\bHW\s*0*(\d+)\b", text, re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1))


def google_document_export(url: str) -> tuple[str, str] | None:
    """
    Convert public Google Slides/Documents URLs into PDF export URLs.
    Returns (export_url, document_id).
    """
    parsed = urlparse(url)

    if parsed.netloc.lower() != "docs.google.com":
        return None

    presentation = re.search(r"/presentation/d/([^/]+)", parsed.path)
    if presentation:
        document_id = presentation.group(1)
        return (
            f"https://docs.google.com/presentation/d/"
            f"{document_id}/export/pdf",
            document_id,
        )

    document = re.search(r"/document/d/([^/]+)", parsed.path)
    if document:
        document_id = document.group(1)
        return (
            f"https://docs.google.com/document/d/"
            f"{document_id}/export?format=pdf",
            document_id,
        )

    return None


print(f"[course] {COURSE_PAGE}")
response = session.get(COURSE_PAGE, timeout=(15, 60))
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

links: list[tuple[str, str]] = []
seen_urls: set[str] = set()

for anchor in soup.select("a[href]"):
    href = anchor.get("href", "").strip()
    if not href:
        continue

    url = urljoin(COURSE_PAGE, href)

    if url.startswith(("mailto:", "javascript:")):
        continue

    if url in seen_urls:
        continue

    seen_urls.add(url)
    links.append((page_context(anchor), url))


downloaded_pdfs: list[tuple[str, Path, str]] = []
downloaded_notebooks: list[tuple[str, Path, str]] = []
video_links: list[tuple[str, str]] = []
external_links: list[tuple[str, str]] = []

used_paths: set[Path] = set()


def allocate_path(directory: Path, filename: str, source_url: str) -> Path:
    path = directory / filename

    if path in used_paths:
        path = directory / (
            f"{path.stem}-{url_hash(source_url)}{path.suffix}"
        )

    used_paths.add(path)
    return path


# 1. Download PDFs hosted directly on the NTU course site.
for label, url in links:
    parsed = urlparse(url)
    path_lower = parsed.path.lower()

    if (
        parsed.netloc.lower() == "speech.ee.ntu.edu.tw"
        and path_lower.endswith(".pdf")
    ):
        basename = safe_filename(Path(unquote(parsed.path)).name)

        if re.match(r"hw\s*0*\d+", basename, re.IGNORECASE):
            output_dir = HOMEWORK_PDF_DIR
        else:
            output_dir = LECTURE_PDF_DIR

        destination = allocate_path(output_dir, basename, url)

        try:
            download_file(url, destination)
            downloaded_pdfs.append((label, destination, url))
        except Exception as error:
            print(f"[error] PDF {url}: {error}")


# 2. Export public Google Slides/Documents as PDFs.
for label, url in links:
    exported = google_document_export(url)
    if exported is None:
        continue

    export_url, document_id = exported
    hw_number = infer_hw_number(label)

    prefix = f"HW{hw_number:02d}" if hw_number is not None else "google"
    filename = f"{prefix}-google-{document_id[:8]}.pdf"

    destination = allocate_path(
        HOMEWORK_PDF_DIR,
        filename,
        url,
    )

    try:
        download_file(export_url, destination)
        downloaded_pdfs.append((label, destination, url))
    except Exception as error:
        print(f"[warning] Google document {url}: {error}")


# 3. Download public Colab notebooks from their Google Drive IDs.
colab_index = 0

for label, url in links:
    parsed = urlparse(url)

    if parsed.netloc.lower() != "colab.research.google.com":
        continue

    match = re.search(r"/drive/([^/?#]+)", parsed.path)
    if not match:
        external_links.append((label, url))
        continue

    drive_id = match.group(1)
    hw_number = infer_hw_number(label)

    if hw_number is not None:
        prefix = f"HW{hw_number:02d}"
    else:
        colab_index += 1
        prefix = f"colab-{colab_index:02d}"

    destination = NOTEBOOK_DIR / f"{prefix}-{drive_id[:8]}.ipynb"

    if destination.exists() and destination.stat().st_size > 0:
        print(f"[skip] {relative(destination)}")
        downloaded_notebooks.append((label, destination, url))
        continue

    print(f"[gdown] {label}")
    try:
        result = gdown.download(
            id=drive_id,
            output=str(destination),
            quiet=False,
        )

        if result is None or not destination.exists():
            raise RuntimeError("gdown did not produce a notebook")

        downloaded_notebooks.append((label, destination, url))
    except Exception as error:
        print(f"[warning] Colab {url}: {error}")

        shortcut = destination.with_suffix(".url.txt")
        shortcut.write_text(url + "\n", encoding="utf-8")


# 4. Catalogue videos and other external resources.
for label, url in links:
    host = urlparse(url).netloc.lower()

    if host in {
        "youtu.be",
        "youtube.com",
        "www.youtube.com",
    }:
        video_links.append((label, url))
        continue

    if (
        host != "speech.ee.ntu.edu.tw"
        and host != "colab.research.google.com"
        and host != "docs.google.com"
    ):
        external_links.append((label, url))


catalog: list[str] = [
    "# Machine Learning 2023 Spring Resource Catalog",
    "",
    f"Official course page: {COURSE_PAGE}",
    "",
    "Generated by `scripts/sync_ml2023_resources.py`.",
    "",
    "## Downloaded lecture PDFs",
    "",
]

for label, path, source in downloaded_pdfs:
    if path.parent != LECTURE_PDF_DIR:
        continue
    catalog.append(
        f"- [{label}]({relative(path)}) — [source]({source})"
    )

catalog.extend(
    [
        "",
        "## Downloaded homework PDFs",
        "",
    ]
)

for label, path, source in downloaded_pdfs:
    if path.parent != HOMEWORK_PDF_DIR:
        continue
    catalog.append(
        f"- [{label}]({relative(path)}) — [source]({source})"
    )

catalog.extend(
    [
        "",
        "## Downloaded Colab notebooks",
        "",
    ]
)

for label, path, source in downloaded_notebooks:
    catalog.append(
        f"- [{label}]({relative(path)}) — [source]({source})"
    )

catalog.extend(
    [
        "",
        "## Lecture and homework videos",
        "",
    ]
)

for label, url in video_links:
    catalog.append(f"- [{label}]({url})")

catalog.extend(
    [
        "",
        "## Other public links",
        "",
    ]
)

for label, url in external_links:
    catalog.append(f"- [{label}]({url})")

CATALOG_PATH.write_text(
    "\n".join(catalog) + "\n",
    encoding="utf-8",
)

print()
print("Sync complete")
print(f"PDFs:      {len(downloaded_pdfs)}")
print(f"Notebooks: {len(downloaded_notebooks)}")
print(f"Videos:    {len(video_links)}")
print(f"Catalog:   {relative(CATALOG_PATH)}")
