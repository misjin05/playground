# Windows에서 Antigravity CLI (`agy`) + EGM → Ralph 파이프라인 구성 및 실험 가이드

이 문서는 Windows 환경에서 **Antigravity CLI (`agy`)**를 기반으로 **EGM(Elephant-Goldfish Model)** 스펙 설계와 **Ralph Loop** 자율 구현을 연결하는 파이프라인을 구성하고, 간단한 예제로 실험해 보는 방법을 정리한 가이드입니다.

---

## 1. 전체 개념 요약

| 단계 | 역할 | 핵심 원칙 |
| :--- | :--- | :--- |
| **EGM (Elephant-Goldfish)** | 스펙 작성 & 다각도 리뷰 게이트 | **Elephant**(긴 컨텍스트)가 초안을 쓰고, **Goldfish**(빈 컨텍스트 서브에이전트)가 모호함을 감사하여 **구현 준비 완료(`Blocker 0`)** 스펙 확정 |
| **Ralph Loop** | 스펙 기반 자율 반복 구현 | 매 반복(Iteration)마다 **새로운 `agy` 세션(Fresh Context)**을 띄워 `PRD.md`에서 태스크 **1개만** 구현 → 테스트 통과 → `git commit` 후 종료 |

### 커버하는 SW 개발 단계 (`Spec-to-Verified-Code`)

단순 `코딩 → 테스트`가 아니라 **요구사항 구체화 · 설계 리뷰 게이트 · 구현 · 테스트 · 자가 수정**까지를 아우릅니다.

1. **흐름도:**
   ```text
   [요구사항·설계] ──▶ [설계 리뷰 게이트] ──▶ [구현 ↔ 테스트 ↔ 수정] ──▶ [검증된 커밋]
    EGM (Elephant)      EGM (Goldfish)           Ralph Loop              Git Main
   ```
2. **단계 요약:**
   > **Design & Spec Review (EGM) → Autonomous Build & Test Loop (Ralph)**
3. **역할 대비:**
   * **EGM (Upstream):** *"올바른 것을 설계했는가?"* (Building the **right** thing)
   * **Ralph (Downstream):** *"설계대로 통과할 때까지 만드는가?"* (Building the thing **right**)

---

## 2. Windows 환경 구성 방법

### Step 1. Antigravity CLI (`agy`) 설치 및 로그인

로컬 **PowerShell**을 열어 `agy` CLI를 설치합니다. (Node.js/Python 런타임이 필요 없는 단일 바이너리로 설치됩니다.)

```powershell
# 1. agy CLI 설치
irm https://antigravity.google/cli/install.ps1 | iex
```

설치 완료 후 **새 PowerShell 창**을 열어 설치 여부와 계정을 연동합니다. (기본 설치 경로: `%LOCALAPPDATA%\agy\bin`)

```powershell
# 2. 설치 확인
agy --version

# 3. 최초 1회 실행하여 Google 계정 OAuth 로그인
agy
```

> 로그인 완료 후 `Ctrl+D` 두 번 또는 `/exit`로 빠져나옵니다.

---

### Step 2. 비대화형(Headless) 실행 테스트

Ralph 루프는 매 회전마다 `agy -p "..."` 형태로 단일 프롬프트를 전달하고 즉시 종료하는 방식을 사용합니다.

```powershell
agy -p "현재 디렉터리 파일 목록만 간단히 알려줘"
```

> **자율 실행 권한 참고:**
> 루프 도중 파일 수정이나 테스트 실행(`pytest` 등)마다 수동 승인으로 멈추지 않으려면, `~/.gemini/antigravity-cli/settings.json`에서 실행 정책을 자동 허용으로 설정하거나 `agy --help`로 자동 승인 관련 플래그를 확인하세요.

---

### Step 3. 루프 실행 도구 선택 (A안 또는 B안)

#### A안. PowerShell 스크립트(`ralph.ps1`) — *가장 심플한 첫 실험용*

별도 패키지 설치 없이 프로젝트 루트에 `ralph.ps1`을 만들어 바로 실행할 수 있습니다.

```powershell
# ralph.ps1
param(
    [int]$MaxIterations = 10
)

for ($i = 1; $i -le $MaxIterations; $i++) {
    Write-Host "=== Ralph Iteration $i / $MaxIterations ===" -ForegroundColor Cyan

    # PRD.md에 미완료 태스크(- [ ])가 없으면 루프 종료
    if (-not (Select-String -Path "PRD.md" -Pattern "- \[ \]" -Quiet)) {
        Write-Host "모든 태스크 완료!" -ForegroundColor Green
        break
    }

    $prompt = Get-Content -Raw "PROMPT.md"
    agy -p $prompt --output-format text

    Start-Sleep -Seconds 2
}
```

#### B안. `ralph-tui` 사용 — *TUI 대시보드 모니터링용*

진행률과 스트림 로그를 터미널 대시보드로 보고 싶을 때 사용합니다. (`bun` 또는 `npm` 필요)

```powershell
# 1. ralph-tui 전역 설치
bun install -g ralph-tui
# 또는 npm install -g ralph-tui

# 2. 프로젝트 루트에서 초기 설정 마법사 실행 (.ralph-tui/config.toml 생성)
ralph-tui setup

# 3. Antigravity 어댑터로 실행
ralph-tui run --prd ./prd.json --agent antigravity
```

---

## 3. 간단한 EGM → Ralph 파이프라인 실험 예시

외부 API나 DB 없이 **`pytest` 결과(Exit Code)만으로 성공/실패가 100% 자동 판별되는 초소형 CLI**가 첫 실험으로 가장 적합합니다.

### 추천 실험 주제: `mdcheck` (로컬 Markdown 링크/헤더 검사기 CLI)

* **기능:** 지정한 폴더 내 `.md` 파일들을 스캔해 **깨진 상대경로 링크**, **존재하지 않는 `#헤더` 앵커**, **중복 헤더**를 찾아 리포트하는 Python CLI
* **이 예제가 좋은 이유:**
  1. 코드블록(```` ``` ````) 내부 링크 무시, GitHub 스타일 헤더 앵커 슬러그 변환, 종료 코드(`0`/`1`/`2`) 규약 등 엣지 케이스가 많아 **EGM의 Goldfish 리뷰 효과**를 체감하기 좋습니다.
  2. `pytest` 통과 여부로 **Ralph 루프의 자동 검증**이 명확합니다.

---

### 실험 디렉터리 구조

```text
my-mdcheck-exp/
├── docs/
│   └── designs/
│       └── mdcheck.md    # [EGM 산출물] Goldfish 리뷰를 통과한 확정 스펙
├── PRD.md                # [Ralph 입력] 체크리스트 태스크
├── progress.txt          # [Ralph 메모리] 이터레이션별 작업 기록
├── PROMPT.md             # [Ralph 지시서] 매 턴 agy에게 전달할 고정 프롬프트
└── ralph.ps1             # 루프 실행 스크립트
```

---

### 4단계 실험 진행 절차

#### 1단계: 프로젝트 초기화

```powershell
mkdir my-mdcheck-exp
cd my-mdcheck-exp
git init
```

#### 2단계: EGM으로 스펙 확정 (`docs/designs/mdcheck.md`)

Antigravity 채팅/IDE에서 다음과 같이 EGM 워크플로우를 실행합니다.

1. **초안 작성 (Elephant):**
   > "로컬 Markdown 파일의 깨진 상대경로 링크, 없는 `#anchor`, 중복 헤더를 검사하는 Python CLI(`mdcheck`) 스펙을 `docs/designs/mdcheck.md`에 작성해줘."
2. **다각도 리뷰 (Goldfish):**
   > `egm-zoom-out`, `egm-design`, `egm-implementation-readiness` 관점으로 스펙을 리뷰해 파일 경로, 함수 시그니처, CLI 옵션(`--format text|json`), 종료 코드, 테스트 케이스의 모호함을 제거(`Blocker 0개` 달성)합니다.

#### 3단계: Ralph 입력 파일 3종 준비

**1) `PRD.md`** (확정된 스펙을 1회전에 1개씩 끝낼 수 있는 작은 단위로 분해)

```markdown
# mdcheck PRD

- [ ] T1: `pyproject.toml`, `src/mdcheck/` 기본 구조 및 CLI 엔트리포인트(`--format text|json`, exit code) + 스모크 테스트
- [ ] T2: 코드블록을 제외한 Markdown 헤더 및 링크 파서 구현 + 단위 테스트
- [ ] T3: 상대경로 파일 존재 여부 및 `#anchor` 슬러그 유효성 검증기 구현 + 단위 테스트
- [ ] T4: 디렉터리 재귀 스캔, 텍스트/JSON 리포터 연결 + 통합 테스트
```

**2) `progress.txt`** (빈 파일로 시작)

```text
# Progress Log
```

**3) `PROMPT.md`** (매 이터레이션 `agy`가 읽을 고정 규칙)

```markdown
1. `docs/designs/mdcheck.md`, `PRD.md`, `progress.txt`를 읽어라.
2. `PRD.md`에서 아직 체크되지 않은(`- [ ]`) 가장 첫 번째 태스크 **딱 1개만** 구현하라.
3. `pytest`를 실행해 모든 테스트가 통과하는지 검증하라. 실패하면 통과할 때까지 수정하라.
4. 모든 테스트가 통과하면 `PRD.md`의 해당 항목을 `- [x]`로 수정하고, `progress.txt`에 완료 내용과 변경 파일을 한 줄 기록한 뒤 `git add -A && git commit -m "<태스크ID>: <요약>"`을 실행하라.
5. 다음 태스크로 넘어가지 말고 즉시 종료하라.
```

초기 파일들을 커밋합니다:

```powershell
git add -A
git commit -m "chore: initialize EGM spec and Ralph loop files"
```

#### 4단계: Ralph 루프 실행

```powershell
./ralph.ps1 -MaxIterations 10
```

실행이 끝나면 `git log --oneline`으로 태스크(`T1`~`T4`)가 각각 독립된 컨텍스트에서 깔끔하게 커밋되었는지, `progress.txt`에 작업 이력이 누적되었는지 확인합니다.
