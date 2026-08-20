#!/usr/bin/env python3
"""Build the shared static webbook site from books/*/book.yaml.

The builder never rewrites Markdown sources. It copies book data into the Pages
artifact, creates JSON manifests, and creates one reader route per book.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

TOP_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$')
ITEM_RE = re.compile(r'^\s*-\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$')
FIELD_RE = re.compile(r'^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$')


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ''
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    low = value.casefold()
    if low == 'true':
        return True
    if low == 'false':
        return False
    if low in {'null', '~'}:
        return None
    return value


def parse_book_yaml(path: Path) -> dict:
    """Parse the conservative subset of YAML used by WEBBOOK_STANDARD.md."""
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    data: dict = {}
    chapters: list[dict] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith('#'):
            i += 1
            continue
        if raw.startswith((' ', '\t')):
            i += 1
            continue
        if stripped == 'chapters:':
            i += 1
            break
        m = TOP_RE.match(raw)
        if not m:
            i += 1
            continue
        key, value = m.groups()
        if value in {'>', '|', '>-', '|-'}:
            block: list[str] = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt and not nxt.startswith((' ', '\t')):
                    break
                block.append(nxt.strip())
                i += 1
            sep = '\n' if value.startswith('|') else ' '
            data[key] = sep.join(x for x in block if x).strip()
            continue
        data[key] = parse_scalar(value)
        i += 1
    current = None
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith('#'):
            i += 1
            continue
        m = ITEM_RE.match(raw)
        if m:
            if current:
                chapters.append(current)
            current = {m.group(1): parse_scalar(m.group(2))}
            i += 1
            continue
        m = FIELD_RE.match(raw)
        if m and current is not None:
            current[m.group(1)] = parse_scalar(m.group(2))
        i += 1
    if current:
        chapters.append(current)
    data['chapters'] = chapters
    return data


def resolve_chapter_file(book_dir: Path, value: str) -> str:
    rel = Path(value)
    if rel.is_absolute() or '..' in rel.parts:
        raise SystemExit(f'Unsafe chapter path in {book_dir / "book.yaml"}: {value}')
    direct = book_dir / rel
    if direct.is_file():
        return rel.as_posix()
    nested = book_dir / 'chapters' / rel
    if nested.is_file():
        return (Path('chapters') / rel).as_posix()
    raise SystemExit(f'Missing chapter file: {value} (book: {book_dir})')


def discover_books(books_root: Path) -> list[tuple[Path, dict]]:
    found = []
    for meta in sorted(books_root.rglob('book.yaml'), key=lambda p: p.as_posix().casefold()):
        book_dir = meta.parent
        book = parse_book_yaml(meta)
        if not book.get('title'):
            raise SystemExit(f'Missing title in {meta}')
        chapters = book.get('chapters') or []
        if not chapters:
            raise SystemExit(f'No chapters in {meta}')
        for chapter in chapters:
            if not chapter.get('file'):
                raise SystemExit(f'Chapter without file in {meta}')
            chapter['file'] = resolve_chapter_file(book_dir, str(chapter['file']))
            if not chapter.get('title'):
                chapter['title'] = chapter.get('id') or Path(chapter['file']).stem
        found.append((book_dir, book))
    return found


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--books', type=Path, default=Path('books'))
    ap.add_argument('--site', type=Path, default=Path('site'))
    ap.add_argument('--output', type=Path, default=Path('_site'))
    args = ap.parse_args()
    books_root = args.books.resolve()
    site_root = args.site.resolve()
    output = args.output.resolve()
    if not books_root.is_dir():
        raise SystemExit(f'Books directory not found: {books_root}')
    if not site_root.is_dir():
        raise SystemExit(f'Site directory not found: {site_root}')
    template_path = site_root / 'book.html'
    if not template_path.is_file():
        raise SystemExit(f'Reader template not found: {template_path}')
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(site_root, output)
    (output / 'book.html').unlink(missing_ok=True)
    shutil.copytree(books_root, output / 'books')
    template = template_path.read_text(encoding='utf-8')
    catalog = []
    for book_dir, book in discover_books(books_root):
        rel = book_dir.relative_to(books_root)
        rel_posix = rel.as_posix()
        depth = len(rel.parts)
        root_prefix = '../' * depth
        route_dir = output / rel
        route_dir.mkdir(parents=True, exist_ok=True)
        chapters = []
        for idx, chapter in enumerate(book['chapters']):
            ch = dict(chapter)
            file_path = str(ch['file'])
            ch['content_url'] = root_prefix + 'books/' + quote(rel_posix) + '/' + '/'.join(quote(part) for part in Path(file_path).parts)
            ch['index'] = idx
            chapters.append(ch)
        public = {k: v for k, v in book.items() if k != 'chapters' and v not in (None, '')}
        public.update({'path': rel_posix, 'url': rel_posix + '/', 'library_url': root_prefix, 'chapters': chapters})
        write_json(route_dir / 'book.json', public)
        page = template.replace('{{ROOT}}', root_prefix).replace('{{BOOK_PATH}}', html.escape(rel_posix, quote=True)).replace('{{BOOK_TITLE}}', html.escape(str(book['title'])))
        (route_dir / 'index.html').write_text(page, encoding='utf-8')
        catalog.append({'title': book['title'], 'category': book.get('category', ''), 'collection': book.get('collection', ''), 'series': book.get('series', ''), 'description': book.get('description', ''), 'language': book.get('language', ''), 'status': book.get('status', ''), 'chapter_count': len(chapters), 'path': rel_posix, 'url': rel_posix + '/'})
    catalog.sort(key=lambda b: (str(b.get('category', '')).casefold(), str(b['title']).casefold()))
    write_json(output / 'catalog.json', catalog)
    print(f'Built {len(catalog)} webbook(s) into {output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
