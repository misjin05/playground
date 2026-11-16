# mdcheck PRD

기준 스펙: [docs/designs/mdcheck.md](docs/designs/mdcheck.md)

- [ ] T1: Package & CLI Scaffold — `pyproject.toml`, `src/mdcheck/__init__.py`, `src/mdcheck/__main__.py`, `src/mdcheck/models.py`, `src/mdcheck/cli.py` 스캐폴드(`--format text|json`, `--version`, exit code `0/1/2`) 및 `tests/test_cli.py` 작성 후 `pytest` 통과
- [ ] T2: Slugifier & Markdown Parser — `src/mdcheck/slug.py` (`slugify`) 및 `src/mdcheck/parser.py` (fenced code block 상태 머신, inline code span 제거, ATX 헤더, inline 링크/이미지 파서) 구현 및 `tests/test_slug.py`, `tests/test_parser.py` 통과
- [ ] T3: File Discovery & Validator — `src/mdcheck/validator.py` (`discover_markdown_files`, `validate_path`, `ParsedDocument` 캐싱, 중복 헤더·상대경로·`#anchor` 검증, 심볼릭 링크/제외 디렉터리 스킵) 구현 및 `tests/test_validator.py` 통과
- [ ] T4: Formatters, CLI Wiring & Integration — `src/mdcheck/formatter.py` (`format_text`, `format_json`), `cli.py` 최종 연결 및 `tests/test_integration.py` 작성 후 전체 `pytest` 통과
