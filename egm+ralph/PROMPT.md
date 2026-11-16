1. `docs/designs/mdcheck.md`, `PRD.md`, `progress.md`를 먼저 읽어라.
2. `PRD.md`에서 아직 체크되지 않은(`- [ ]`) 가장 첫 번째 태스크 **딱 1개만** 선택해 `docs/designs/mdcheck.md`의 파일 경로, 함수 시그니처, 스키마, 엣지 케이스 규약에 정확히 맞춰 구현하라.
3. 필요한 경우 `pip install -e .[dev]`로 개발 모드로 설치한 뒤 `python -m pytest`를 실행해 모든 테스트가 통과하는지 검증하라. 실패하면 통과할 때까지 수정하라.
4. 모든 테스트가 통과하면:
   - `PRD.md`에서 이번에 완료한 태스크 1개만 `- [x]`로 표시하라.
   - `progress.md`에 이터레이션 기록(태스크 ID, 요약, 변경/생성 파일, `pytest` 결과)을 추가하라.
   - `git add -A && git commit -m "<태스크ID>: <한줄 요약>"`을 실행해 커밋하라.
5. 다음 태스크로 절대 넘어가지 말고 즉시 종료하라.
