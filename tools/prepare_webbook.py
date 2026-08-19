#!/usr/bin/env python3
"""Prepare a webbook publication directory without rewriting Markdown bodies.

The tool copies source Markdown bytes unchanged, normalizes publication filenames,
and writes a minimal book.yaml. It is intentionally conservative: it never replaces
an existing destination file with different bytes.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

INVALID = re.compile(r'[\\/:*?"<>|#%]')
DECORATIVE = str.maketrans('', '', '「」『』‘’“”')
H1_RE = re.compile(r'^#\s+(.+?)\s*$', re.MULTILINE)
SECTION_RE = re.compile(r'^\s*(\d+)\.(\d+)\s*[-–—.:：]?\s*(.*)$')
JE_RE = re.compile(r'^\s*제\s*(\d+)\s*(경|장|절|권)\s*[-–—.:：]?\s*(.*)$')
NUMBER_RE = re.compile(r'^\s*(\d+)\s*[-–—.:：]?\s*(.*)$')


@dataclass(frozen=True)
class Chapter:
    source: Path
    source_name: str
    title: str
    ident: str
    publish_name: str


def safe_extract(zf: zipfile.ZipFile, dest: Path) -> None:
    root = dest.resolve()
    for info in zf.infolist():
        name = info.filename.replace('\\', '/')
        if name.startswith('/') or '..' in Path(name).parts:
            raise SystemExit(f'Unsafe ZIP path: {info.filename}')
        target = (dest / name).resolve()
        if root != target and root not in target.parents:
            raise SystemExit(f'Unsafe ZIP path: {info.filename}')
    zf.extractall(dest)


def markdown_files(root: Path) -> list[Path]:
    files = []
    for p in root.rglob('*.md'):
        if any(part.startswith('.') for part in p.relative_to(root).parts):
            continue
        if '__MACOSX' in p.parts:
            continue
        files.append(p)
    return sorted(files, key=lambda p: str(p).casefold())


def read_h1(path: Path) -> str | None:
    raw = path.read_bytes()
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        return None
    m = H1_RE.search(text)
    return m.group(1).strip() if m else None


def sanitize_title(text: str) -> str:
    text = text.translate(DECORATIVE)
    text = INVALID.sub('', text)
    text = re.sub(r'[()（）\[\]{}]+', '', text)
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'_+', '_', text).strip('._-')
    return text or 'untitled'


def numeric_width(values: Iterable[int], count: int) -> int:
    maximum = max(values, default=0)
    n = max(maximum, count)
    if n >= 1000:
        return 4
    if n >= 100:
        return 3
    return 2


def parse_title(h1: str | None, fallback: str):
    title = h1.strip() if h1 else fallback.strip()
    m = SECTION_RE.match(title)
    if m:
        a, b, rest = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        return ('section', (a, b), rest or title)
    m = JE_RE.match(title)
    if m:
        n, rest = int(m.group(1)), m.group(3).strip()
        return ('number', n, rest or title)
    m = NUMBER_RE.match(title)
    if m:
        n, rest = int(m.group(1)), m.group(2).strip()
        return ('number', n, rest or title)
    return ('none', None, title)


def yaml_quote(s: str) -> str:
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def build_chapters(files: list[Path]) -> list[Chapter]:
    parsed = []
    plain_numbers = []
    for p in files:
        h1 = read_h1(p)
        fallback = p.stem
        kind, number, cleaned_title = parse_title(h1, fallback)
        if kind == 'number':
            plain_numbers.append(number)
        parsed.append((p, h1 or fallback, kind, number, cleaned_title))

    width = numeric_width(plain_numbers, len(files))
    chapters = []
    seen = set()
    for p, display_title, kind, number, cleaned_title in parsed:
        if kind == 'section':
            a, b = number
            ident = f'{a:02d}-{b:02d}'
            name = f'{ident}_{sanitize_title(cleaned_title)}.md'
        elif kind == 'number':
            ident = f'{number:0{width}d}'
            name = f'{ident}_{sanitize_title(cleaned_title)}.md'
        else:
            ident = sanitize_title(p.stem)
            name = f'{sanitize_title(p.stem)}.md'

        key = name.casefold()
        if key in seen:
            raise SystemExit(f'Publication filename collision: {name}')
        seen.add(key)
        chapters.append(Chapter(p, p.name, display_title, ident, name))

    def sort_key(c: Chapter):
        parts = re.findall(r'\d+', c.ident)
        return (0, tuple(map(int, parts))) if parts else (1, c.ident.casefold())

    return sorted(chapters, key=sort_key)


def write_book_yaml(dest: Path, args, chapters: list[Chapter]) -> None:
    lines = [
        f'title: {yaml_quote(args.title)}',
        f'category: {yaml_quote(args.category)}',
    ]
    if args.collection:
        lines.append(f'collection: {yaml_quote(args.collection)}')
    if args.series:
        lines.append(f'series: {yaml_quote(args.series)}')
    if args.description:
        lines.append(f'description: {yaml_quote(args.description)}')
    lines.extend([
        'language: "ko"',
        f'status: {yaml_quote(args.status)}',
        '',
        'chapters:',
    ])
    for c in chapters:
        lines.extend([
            f'  - id: {yaml_quote(c.ident)}',
            f'    title: {yaml_quote(c.title)}',
            f'    file: {yaml_quote(c.publish_name)}',
            f'    source_file: {yaml_quote(c.source_name)}',
        ])
    dest.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--zip', dest='zip_path', type=Path)
    group.add_argument('--input-dir', type=Path)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--category', default='기타')
    ap.add_argument('--collection', default='')
    ap.add_argument('--series', default='')
    ap.add_argument('--description', default='')
    ap.add_argument('--status', default='ongoing')
    args = ap.parse_args()

    with tempfile.TemporaryDirectory(prefix='webbook-') as tmp:
        if args.zip_path:
            source_root = Path(tmp) / 'source'
            source_root.mkdir()
            with zipfile.ZipFile(args.zip_path) as zf:
                safe_extract(zf, source_root)
        else:
            source_root = args.input_dir

        files = markdown_files(source_root)
        if not files:
            raise SystemExit('No Markdown files found.')
        chapters = build_chapters(files)

        out = args.output_dir
        out.mkdir(parents=True, exist_ok=True)
        for c in chapters:
            target = out / c.publish_name
            source_bytes = c.source.read_bytes()
            if target.exists():
                if target.read_bytes() != source_bytes:
                    raise SystemExit(f'Refusing to overwrite different file: {target}')
                continue
            target.write_bytes(source_bytes)

        yaml_path = out / 'book.yaml'
        if yaml_path.exists():
            raise SystemExit(f'Refusing to overwrite existing metadata: {yaml_path}')
        write_book_yaml(yaml_path, args, chapters)

        print(f'Prepared {len(chapters)} Markdown files in {out}')
        for c in chapters:
            print(f'{c.source_name} -> {c.publish_name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
