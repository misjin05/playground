# mdcheck: Local Markdown Link & Header Checker CLI

*   **Author:** hyejin05-lee
*   **Status:** Approved
*   **Date:** 2026-11-16

--------------------------------------------------------------------------------

## Overview

`mdcheck` is a local, offline Python (`>= 3.10`) command-line tool that scans Markdown (`.md`) files in a target directory or single file and reports broken relative file links, missing `#anchor` fragment targets, and duplicate headings. It uses only the Python standard library at runtime, outputs deterministic `text` or `json` reports to `stdout`, and returns predictable exit codes (`0`, `1`, `2`) for local development and CI pipelines.

## The Problem

Markdown documentation in repositories frequently breaks silently when files are moved, renamed, or refactored:

1. Relative links (`./other.md`, `../docs/spec.md`) point to deleted or renamed files.
2. Fragment links (`[section](#my-heading)` or `other.md#my-heading`) reference headings that were renamed or removed.
3. Duplicate headings within a single file cause ambiguous anchor targets, and naive regex scanners produce false positives on link-like syntax inside fenced or inline code blocks.

Without an offline, deterministic checker, these broken references accumulate until readers encounter dead links. `mdcheck` solves this by parsing a well-defined Markdown subset while ignoring code blocks, validating local file and anchor targets, and reporting sorted diagnostics.

## Goals

*   **G1 — Accurate Local Link Validation:** Detect broken relative file and image paths (`[text](path)` and `![alt](path)`) resolved relative to the source `.md` file's directory.
*   **G2 — Anchor & Duplicate Heading Validation:** Validate `#anchor` targets (same-file and cross-file `path.md#anchor`) against normalized heading slugs, and report duplicate headings within the same file.
*   **G3 — Code-Block-Aware Parsing:** Ignore headings and links inside fenced code blocks (```` ``` ```` / `~~~`) and inline code spans (`` `...` ``).
*   **G4 — Deterministic CLI & Output:** Support `mdcheck <path> [--format {text,json}] [--version]`, route lint output to `stdout` and errors to `stderr`, sort issues deterministically, and return exit codes `0`, `1`, or `2`.
*   **G5 — Testable, Zero-Runtime-Dependency Design:** Run completely offline using only the Python standard library, verified by `pytest`.

## Non-Goals

*   **NG1 — External URL Checking:** `mdcheck` does not make network requests or validate `http://`, `https://`, `mailto:`, `tel:`, `data:`, or `ftp://` targets.
*   **NG2 — Auto-Fixing / Rewriting Files:** `mdcheck` is read-only and never modifies `.md` files.
*   **NG3 — Full CommonMark / HTML Rendering:** `mdcheck` does not render HTML, parse raw HTML `<a href>` / `<h1 id>` tags, or support Setext (`===`/`---`) headings or reference-style (`[text][ref]`) links.

## Design Decisions (Resolved)

| Topic | Decision | Rationale |
| :--- | :--- | :--- |
| **Runtime & Parser** | Python `>= 3.10`, stdlib only (`argparse`, `dataclasses`, `json`, `pathlib`, `re`, `unicodedata`, `urllib.parse`). | Zero install friction in CI/local environments; bounded Markdown subset avoids a custom CommonMark engine. |
| **Image Links** | Validate local relative `![alt](path)` paths for file existence using the same target rules as `[text](path)`. | Broken local image paths are a common documentation defect with identical resolution logic. |
| **Duplicate Headings vs. Slug Suffixes** | Duplicate headings (matching normalized slug within the same file) emit `duplicate-heading` (exit `1`). GitHub `-1`/`-2` suffixes are **not** generated. | Treating duplicates as errors makes `-1`/`-2` disambiguation suffixes contradictory and unnecessary (YAGNI). |
| **Excluded Directories** | Hardcode `DEFAULT_EXCLUDED_DIRS = frozenset({".git", ".venv", "venv", "node_modules", "__pycache__"})`. No `--exclude` flag in v1. | Covers standard repo/env directories without speculative CLI configuration. |

## Critical User Journeys (CUJs)

### CUJ 1: Local Directory Check in Text Format

*   **Given**: A directory containing `.md` files where `README.md` has a broken relative link `./missing.md` on line 12 and `docs/guide.md` has a duplicate `## Setup` heading on line 20.
*   **When**: The user runs `mdcheck .` (default `--format text`).
*   **Then**: `mdcheck` prints sorted issues to `stdout` (`docs/guide.md:20: [duplicate-heading] ...`, `README.md:12: [broken-link] ...`) and exits with code `1`.

### CUJ 2: CI / Scripted Check in JSON Format

*   **Given**: A directory with valid relative links, valid `#anchor` fragments, and broken-looking links inside fenced code blocks.
*   **When**: A CI script runs `mdcheck ./docs --format json`.
*   **Then**: `mdcheck` ignores code-block content, writes a valid JSON object (`issue_count: 0`, `issues: []`) to `stdout`, and exits with code `0`.

### CUJ 3: Invalid CLI Input or I/O Error

*   **Given**: The user passes a non-existent path `./does-not-exist`, a non-`.md` file `./notes.txt`, or an unsupported `--format xml`.
*   **When**: The user runs `mdcheck <invalid-input>`.
*   **Then**: `mdcheck` writes an error message to `stderr` (nothing to `stdout`) and exits with code `2`.

## Technical Plan (Architecture)

### Package & File Boundary

```text
my-mdcheck-exp/
├── pyproject.toml
├── src/
│   └── mdcheck/
│       ├── __init__.py      # Package version (__version__ = "0.1.0")
│       ├── __main__.py      # `python -m mdcheck` entry point
│       ├── cli.py           # argparse CLI, error handling, exit code dispatch
│       ├── models.py        # IssueCode, Heading, LinkRef, ParsedDocument, Issue, CheckReport
│       ├── slug.py          # GitHub-style Unicode slugify()
│       ├── parser.py        # Code-block-aware ATX heading & inline link extractor
│       ├── validator.py     # File discovery, caching, duplicate/link/anchor validation
│       └── formatter.py     # Deterministic text and JSON formatters
└── tests/
    ├── test_cli.py          # CLI flags, exit codes (0/1/2), stdout/stderr routing
    ├── test_parser.py       # Fenced blocks, inline code, ATX headings, link variants
    ├── test_slug.py         # ASCII, Unicode/Korean, punctuation, inline formatting
    ├── test_validator.py    # Relative paths, anchors, duplicates, caching, symlinks
    └── test_integration.py  # End-to-end directory & JSON/text output tests
```

### Data Flow

```text
[CLI args] ─▶ cli.main()
                 │
                 ├─▶ validator.discover_markdown_files(target)
                 │      └─ sorted .md paths (skips DEFAULT_EXCLUDED_DIRS & symlinks)
                 │
                 ├─▶ validator.validate_path(target)
                 │      ├─ parser.parse_markdown(text) ─▶ ParsedDocument(headings, links)
                 │      ├─ slug.slugify(heading.text)  ─▶ duplicate-heading check
                 │      └─ resolve target path & #frag ─▶ broken-link / missing-anchor
                 │                                        (with per-Path ParsedDocument cache)
                 │
                 └─▶ formatter.format_text / format_json ─▶ stdout (exit 0 or 1)
                                                         └─ stderr on CLI/I/O error (exit 2)
```

## Alternatives Considered

### Alternative A: Wrap External Tools (`lychee` or `markdown-link-check`)

*   **Pros**: Mature link checkers with built-in concurrency and external URL support.
*   **Cons**: Requires Rust/Node.js runtime or external binary installation on Windows, and does not enforce duplicate-heading rules or a zero-dependency Python `pytest` workflow.
*   **Reason for Rejection**: Violates the zero-external-runtime Python CLI requirement and adds non-Python toolchain friction.

### Alternative B: Third-Party CommonMark AST Library (`markdown-it-py` or `mistune`)

*   **Pros**: Handles full CommonMark edge cases (nested blockquotes, Setext headings, reference links) out of the box.
*   **Cons**: Introduces third-party runtime dependencies that must be installed before running `mdcheck` and adds AST traversal complexity for features outside v1 scope.
*   **Reason for Rejection**: A bounded line-state parser in Python stdlib covers fenced/inline code blocks, ATX headings, and inline links with zero runtime dependencies.

## Risks & Mitigations

| Risk / Failure Mode | Impact | Mitigation |
| :--- | :--- | :--- |
| **Symlink directory loops** | Infinite recursion during `rglob`/traversal. | Skip symlinked files and directories (`Path.is_symlink()`) during discovery. |
| **Non-UTF-8 or unreadable `.md` files** | Unhandled `UnicodeDecodeError` or `OSError` crash. | Catch `OSError` and `UnicodeDecodeError` in `validator`, record an I/O error message to `stderr`, and return exit code `2` (`2 > 1 > 0`). |
| **Repeated parsing of shared targets (`README.md`)** | $O(N \cdot M)$ slowdown on cross-file `#anchor` links. | Cache `ParsedDocument` per resolved `Path` inside `validate_path()` so every file is read and parsed at most once. |
| **OS-dependent filesystem traversal order** | Non-deterministic output across Windows and Linux. | Sort discovered paths lexicographically by `as_posix()` and sort `issues` by `(file, line, code, target)`. |

## Detailed Implementation

### 1. Packaging (`pyproject.toml`)

*   Build system: `setuptools>=68.0` (`setuptools.build_meta`), package directory `src`.
*   `name = "mdcheck"`, `version = "0.1.0"`, `requires-python = ">=3.10"`, `dependencies = []`.
*   `[project.optional-dependencies]`: `dev = ["pytest>=7.0"]`.
*   `[project.scripts]`: `mdcheck = "mdcheck.cli:main"`.

### 2. Data Models (`src/mdcheck/models.py`)

```python
from dataclasses import dataclass
from enum import Enum

class IssueCode(str, Enum):
    BROKEN_LINK = "broken-link"
    MISSING_ANCHOR = "missing-anchor"
    DUPLICATE_HEADING = "duplicate-heading"

@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    text: str
    slug: str

@dataclass(frozen=True)
class LinkRef:
    line: int
    raw_target: str
    is_image: bool

@dataclass(frozen=True)
class ParsedDocument:
    headings: tuple[Heading, ...]
    links: tuple[LinkRef, ...]

@dataclass(frozen=True)
class Issue:
    file: str       # POSIX relative path from base root (or filename if single file)
    line: int
    code: IssueCode
    target: str     # Raw link target or normalized heading slug
    message: str

@dataclass(frozen=True)
class CheckReport:
    target: str
    files_checked: int
    issues: tuple[Issue, ...]
```

### 3. Slug Normalization (`src/mdcheck/slug.py`)

*   Signature: `def slugify(text: str) -> str:`
*   Exact normalization steps:
    1. Strip inline link/image wrappers: replace `![alt](url)` with `alt` and `[label](url)` with `label`.
    2. Remove inline code backticks `` ` `` and `*` characters while preserving `_`, then normalize with `unicodedata.normalize("NFKC", cleaned).strip().lower()`.
    3. Remove every character except Unicode alphanumeric (`ch.isalnum()`), whitespace (`ch.isspace()`), hyphen (`'-'`), and underscore (`'_'`).
    4. Replace each whitespace character with `'-'` (e.g., `"A & B"` -> `"a--b"`, matching GitHub's behavior where `&` is stripped leaving two spaces -> `--`).
    5. Return the resulting string without stripping leading or trailing `'-'`.

### 4. Markdown Parser (`src/mdcheck/parser.py`)

*   Signature: `def parse_markdown(text: str) -> ParsedDocument:`
*   **Fenced code block state machine:**
    *   Track `fence_char: str | None` (`'`'` or `'~'`) and `fence_len: int`.
    *   A line matching `^\s{0,3}(`{3,}|~{3,})(.*)$` opens a fence if `fence_char is None` (note: backtick fences cannot contain `` ` `` in the info string). While inside a fence, a line matching `^\s{0,3}([`~]+)\s*$` with the same char and `len >= fence_len` closes it.
    *   All lines inside a fence are skipped.
*   **ATX Headings:**
    *   On non-fenced lines, match `^\s{0,3}(#{1,6})\s+(.+?)(?:\s+#+\s*)?$`.
    *   Create `Heading(line=lineno, level=len(hashes), text=raw_text.strip(), slug=slugify(raw_text))`.
*   **Inline Code Span Stripping & Links:**
    *   On every non-fenced line (including ATX heading lines, after `slugify(raw_text)` has been computed), strip inline code spans matched by `` (`+)(.+?)\1 `` (replacing with empty string or spaces).
    *   Match inline links and images: `(!?)\[([^\]]*)\]\(([^)]+)\)` (ignoring escaped `\[` / `\]`).
    *   For `raw_target` inside `(...)`:
        *   Call `raw_target = raw_target.strip()`.
        *   If `raw_target` starts with `<` and contains `>`, extract content between `<` and `>` as `target`.
        *   Otherwise, `parts = raw_target.split(None, 1)` and `target = parts[0] if parts else ""` to strip optional `"title"` / `'title'`.
        *   Record `LinkRef(line=lineno, raw_target=target, is_image=(bang == "!"))`.

### 5. Validator & File Discovery (`src/mdcheck/validator.py`)

*   Constants:
    *   `DEFAULT_EXCLUDED_DIRS = frozenset({".git", ".venv", "venv", "node_modules", "__pycache__"})`
    *   `IGNORED_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "ftp://")`
*   Signatures:
    *   `def discover_markdown_files(target: Path) -> list[Path]:`
        *   If `target.is_file()`: if `target.suffix.lower() != ".md"` raise `ValueError(f"Not a Markdown file: {target}")`; return `[target]`.
        *   If `target.is_dir()`: recursively walk, pruning any directory in `DEFAULT_EXCLUDED_DIRS` or `is_symlink()`. Collect non-symlink files with `suffix.lower() == ".md"`, sorted by `path.as_posix()`.
        *   Otherwise raise `FileNotFoundError(f"Path not found: {target}")`.
    *   `def validate_path(target: Path) -> CheckReport:`
        *   Discover files (`files`). Maintain `doc_cache: dict[Path, ParsedDocument] = {}`.
        *   Helper `get_doc(path: Path) -> ParsedDocument`: reads `path.read_text(encoding="utf-8")`, parses via `parse_markdown`, caches by `path.resolve()`. (Propagates `OSError` / `UnicodeDecodeError` to `cli.main()` for exit code `2`.)
        *   Determine `base_dir = target if target.is_dir() else target.parent`. Display path = `file.relative_to(base_dir).as_posix()`.
        *   **Duplicate headings:** Track `seen_slugs: set[str]` per file. If `heading.slug` is already in `seen_slugs` (and non-empty), emit `Issue(file=rel, line=heading.line, code=IssueCode.DUPLICATE_HEADING, target=heading.slug, message=f"Duplicate heading: {heading.text!r} (#{heading.slug})")`.
        *   **Links:** For each `link` in `doc.links`:
            1. Skip if `link.raw_target.lower().startswith(IGNORED_SCHEMES)` or `link.raw_target == ""`.
            2. Split on `#` (`maxsplit=1`) -> `(raw_path, fragment)` (`fragment` is `None` if no `#`).
            3. Strip `?query` from `raw_path`, then `rel_path = urllib.parse.unquote(raw_path)`. If `fragment is not None`, set `fragment = urllib.parse.unquote(fragment)`.
            4. If `rel_path == ""` (same-file `#anchor`): target file is `current_file`. Check `fragment` against `{h.slug for h in doc.headings}`; if missing (including empty `#` where `fragment == ""`), emit `MISSING_ANCHOR` with `message=f"Missing anchor: #{fragment}"`.
            5. If `rel_path.startswith("/")` (root-relative): emit `BROKEN_LINK` (`message=f"Target not found: {link.raw_target}"`).
            6. Otherwise resolve `resolved = (current_file.parent / rel_path).resolve()`. If `not resolved.exists()` (relative links to existing directories such as `./docs/` are valid): emit `BROKEN_LINK` (`message=f"Target not found: {link.raw_target}"`).
            7. Else if `fragment is not None` and `not link.is_image` and `resolved.suffix.lower() == ".md"` and `resolved.is_file()`: load `target_doc = get_doc(resolved)` (on-demand even for single-file runs); if `fragment` not in `{h.slug for h in target_doc.headings}` (including empty `#`), emit `MISSING_ANCHOR` (`message=f"Missing anchor: #{fragment}"`).
        *   Sort `issues` by `(i.file, i.line, i.code.value, i.target)` and return `CheckReport(target=target.as_posix(), files_checked=len(files), issues=tuple(issues))`.

### 6. Formatters & CLI (`src/mdcheck/formatter.py`, `src/mdcheck/cli.py`)

*   `format_text(report: CheckReport) -> str`:
    *   If `report.issues`: join `f"{i.file}:{i.line}: [{i.code.value}] {i.message}"` with `"\n"`.
    *   Else: `f"OK: {report.files_checked} file(s) checked, 0 issues."`
*   `format_json(report: CheckReport) -> str`:
    *   `json.dumps` (with `indent=2`, `ensure_ascii=False`) of:
        ```json
        {
          "version": "1",
          "target": "<report.target>",
          "files_checked": 0,
          "issue_count": 0,
          "issues": [
            {
              "file": "...",
              "line": 1,
              "code": "broken-link",
              "target": "...",
              "message": "..."
            }
          ]
        }
        ```
*   `cli.main(argv: list[str] | None = None) -> int`:
    *   `argparse.ArgumentParser(prog="mdcheck")` with positional `path` (required `Path`), `--format` (`choices=["text", "json"]`, `default="text"`), `--version` (`action="version"`, `version=f"%(prog)s {__version__}"`). Invalid CLI args exit `2` via `argparse`.
    *   Catch `(FileNotFoundError, ValueError, OSError, UnicodeDecodeError)` -> print `f"Error: {exc}"` to `sys.stderr`, return `2`.
    *   Print `format_json(report)` or `format_text(report)` to `sys.stdout`.
    *   Return `1` if `report.issues` else `0`.

## Test Plan

| Test File | Test Cases (Happy Path & Edge Cases) |
| :--- | :--- |
| `tests/test_cli.py` | `--version` exits `0`; invalid `--format xml` exits `2` to `stderr`; missing path exits `2`; non-`.md` single file exits `2`; empty directory exits `0`; `text` vs `json` output routed to `stdout`. |
| `tests/test_slug.py` | ASCII headings (`"Hello World"` -> `"hello-world"`), punctuation (`"A & B"` -> `"a--b"`), Korean/Unicode (`"설치 방법"` -> `"설치-방법"`), inline formatting (`"Use \`foo\`"` -> `"use-foo"`). |
| `tests/test_parser.py` | Ignores links/headings inside ```` ``` ```` and `~~~` (including nested/longer fences); ignores inline code `` `[bad](./x.md)` ``; parses ATX `h1`–`h6` with trailing `#`; parses `[t](<a b.md>)`, `[t](./a.md "title")`, and `![img](./a.png)`. |
| `tests/test_validator.py` | Valid/broken relative links; URL-encoded `%20` paths; external `https://`/`mailto:` ignored; same-file & cross-file `#anchor` (including single-file `mdcheck a.md` -> `b.md#sec`); duplicate headings (exact & case-insensitive) emit `duplicate-heading`; `.git`/`.venv` skipped; symlinks skipped; UTF-8 decode error raises for exit `2`. |
| `tests/test_integration.py` | End-to-end temp repo fixture via `cli.main([str(tmp_path), "--format", "json"])` verifying exact JSON schema, deterministic sort order, and exit code `1` -> fixed `0`. |

## Phasing & Checkpoints

*   **Phase 1 (`T1`): Package & CLI Scaffold** — `pyproject.toml`, `models.py`, `cli.py`, `__init__.py`, `__main__.py`, and `tests/test_cli.py`. Verify: `pytest tests/test_cli.py`.
*   **Phase 2 (`T2`): Slugifier & Parser** — `slug.py`, `parser.py`, `tests/test_slug.py`, `tests/test_parser.py`. Verify: `pytest tests/test_slug.py tests/test_parser.py`.
*   **Phase 3 (`T3`): Validator** — `validator.py`, `tests/test_validator.py`. Verify: `pytest tests/test_validator.py`.
*   **Phase 4 (`T4`): Formatters & Integration** — `formatter.py`, wire `cli.py`, `tests/test_integration.py`. Verify: `pytest` (all tests pass).
