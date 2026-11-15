# EGM (Elephant-Goldfish Model) & Ralph Loop 가이드

이 문서는 **EGM (`egm.dev`)** 사용법과 **Loop Engineering / Ralph Loop** 개념, 실전 연계 방법 및 참고 링크를 정리한 가이드입니다.

> 📌 **Windows `agy` + EGM → Ralph 환경 구성 및 실험 가이드:** [README.md](./README.md)

---

## 1. EGM (https://egm.dev) 개요

**EGM (Elephant-Goldfish Model)**은 Google 엔지니어링 출신 Dave Rensin의 에세이에서 출발한 **Spec-Driven Development(명세 기반 개발)** 오픈소스 플러그인입니다.  
AI가 처음부터 무작정 코드를 짜다가 발생하는 오류와 환각을 줄이기 위해, **코드 작성 전 설계 문서(Spec)를 먼저 작성하고 독립된 서브에이전트로 검증**하도록 돕습니다.

### 핵심 개념: 코끼리와 금붕어

| 역할 | 컨텍스트 | 책임 |
| :--- | :--- | :--- |
| 🐘 **코끼리 (Elephant)** | 프로젝트 배경, 요구사항, 이전 대화 맥락 전체 보유 | 사용자와 브레인스토밍하고 상세 설계서(`design_draft.md`)를 작성 |
| 🐠 **금붕어 (Goldfish)** | **이전 대화 기억 없음** (문서와 코드 원본만 확인) | 백지 상태에서 편향 없이 빈틈, 엣지 케이스, 구현 리스크를 비판/검토 |
| 👤 **사용자 (You)** | 목표 및 제약 조건 | 리뷰 결과를 보고 아키텍처 트레이드오프를 결정하고 최종 승인 |

---

## 2. EGM 슬래시 명령어별 사용 예제

Antigravity / Claude Code 환경에서 `/egm:명령어` 형태로 호출합니다.

### 2-1. 신규 기능 설계 워크플로우

#### ① `/egm:egm-brainstorm` — 아이디어 발굴 및 구체화
모호한 아이디어를 대화형 질의응답으로 엣지 케이스까지 파고들어 `concepts_brief.md`로 정리합니다.
```text
/egm:egm-brainstorm 결제 실패 시 지수 백오프로 재시도하고 슬랙으로 알림을 보내는 워커 시스템 구축
```
```text
/egm:egm-brainstorm 멀티 테넌트 B2B SaaS를 위한 역할 기반 접근 제어(RBAC) 시스템
```

#### ② `/egm:egm-draft` — 상세 설계서 초안 작성
브레인스토밍 결과물(`concepts_brief.md`)을 바탕으로 구조화된 기술 설계 문서(`design_draft.md`)를 섹션별로 작성합니다.
```text
/egm:egm-draft
```
```text
/egm:egm-draft ./docs/briefs/payment_worker.md
```

#### ③ `/egm:egm-review` — 금붕어 피어 리뷰 실행
이전 대화 맥락이 없는 독립 서브에이전트(Goldfish)들을 호출하여 설계 문서의 약점을 5단계로 감사(Audit)합니다. (빈말/칭찬 금지 규칙 적용)
```text
/egm:egm-review design_draft.md
```
```text
/egm:egm-review docs/designs/auth_architecture.md
```

#### ④ `/egm:egm-resolve` — 리뷰 지적사항 반영 및 조율
금붕어 리뷰어들이 지적한 문제점들을 코끼리(메인 에이전트)와 함께 검토하며 설계 문서를 패치합니다.
```text
/egm:egm-resolve
```
```text
/egm:egm-resolve TargetFile="design_draft.md"
```

### 2-2. 특정 문서 감사 & 기존 코드베이스 관리

#### ⑤ `/egm:egm-review-loop` — 맞춤형 문서 검토 루프
README, PR 계획서, API 명세서 등 임의의 마크다운 문서를 지정된 잣대로 반복 감사/수정할 때 사용합니다.
```text
/egm:egm-review-loop README.md
```
```text
/egm:egm-review-loop docs/api/v2_spec.md
```

#### ⑥ `/egm:egm-bootstrap` — 기존 코드베이스 분석 및 README 생성
기존 레포지토리를 스캔하여 폴더별/컴포넌트별 계약(Interface, Invariant)이 명시된 EGM 표준 `README.md`를 생성합니다.
```text
/egm:egm-bootstrap .
```
```text
/egm:egm-bootstrap src/services/billing
```

#### ⑦ `/egm:egm-drift-report` — 설계 문서와 실제 코드 간 괴리 탐지
시간이 지나 코드가 수정되면서 설계 문서와 달라진 부분(Drift)을 찾아 `{YYYY-MM-DD}_DRIFT_REPORT.md`로 보고합니다.
```text
/egm:egm-drift-report docs/designs/
```

---

## 3. Loop Engineering & 관련 도구 키워드

**Loop Engineering**은 사람이 매 턴 프롬프트를 입력하는 대신, 에이전트가 스스로 **`코드 작성 → 테스트/린트 실행 → 에러 확인 → 수정`** 루프를 목표 달성까지 반복하도록 시스템을 설계하는 개발 패러다임입니다.

### 자주 함께 언급되는 유사 이름 도구들
1. **Hydrogen (`Gemini 4 Hydrogen`)**: Google의 고속 에이전트 코딩 모델 (병렬 툴 호출 및 빠른 루프 실행에 특화).
2. **Hydron (`H2Loop`)**: STM32, ESP32, RISC-V 등 임베디드/펌웨어 개발용 하드웨어 인식 AI 코딩 에이전트(내장 빌드 루프).
3. **Hydra**: 코딩 에이전트를 Docker 컨테이너나 브랜치별 병렬 세션으로 격리해 실행하는 샌드박스·오케스트레이션 도구군.

### Loop Engineering의 핵심 안전장치
* **비용/토큰 상한(Budget Cap):** 무한 루프로 인한 비용 폭주 방지 (`max_iterations` 설정)
* **객관적 검증 게이트(Verifier Gate):** AI의 주관적 판단이 아니라 실제 `pytest`, `pnpm test` 통과 여부로 완료 판정
* **격리 및 롤백:** Git 브랜치 단위 격리로 실패 시 안전하게 원복

---

## 4. Ralph Loop (랄프 루프)

**Ralph Loop**는 Geoffrey Huntley가 제안한 자율 코딩 패턴으로, 한 대화창이 길어질수록 AI 성능이 떨어지는 **Context Rot(컨텍스트 오염)**을 해결하기 위해 등장했습니다.

### 핵심 원리
대화를 길게 이어가지 않고 **작업 1개를 끝낼 때마다 AI 세션을 완전히 종료하고 새 세션(Fresh Context)으로 다시 시작**합니다. 기억은 대화가 아니라 **디스크의 파일과 Git 기록**에만 남깁니다.

```bash
for i in $(seq 1 15); do
  cat PROMPT.md | claude -p --dangerously-skip-permissions
  if grep -q "ALL_TASKS_DONE" progress.md; then
    break
  fi
done
```

### 제대로 돌아가게 하는 4가지 핵심 파일
1. **`PRD.md` (또는 `tasks.json`) — 할 일 목록:** 구현할 기능과 완료 기준을 1회 루프(1커밋) 크기로 작게 쪼갠 체크리스트
2. **`PROMPT.md` — 매 턴 고정 지시서:** *"PRD와 progress를 읽고, 미완료 태스크 딱 1개만 구현하고, 테스트를 통과시킨 뒤 커밋하고 종료하라"*
3. **`progress.md` — 인수인계 파일:** 새 세션으로 켜진 다음 루프의 에이전트가 이전 맥락과 주의점을 빠르게 파악하도록 남기는 메모
4. **자동 검증 수단 (Tests / Lint / Typecheck):** `pytest`, `tsc`, `pnpm test` 등 객관적인 통과 기준

---

## 5. EGM을 통해 Ralph 4가지 핵심 파일 만들기

EGM과 Ralph Loop를 결합하면 **설계(EGM) → 자율 구현(Ralph)** 파이프라인을 구축할 수 있습니다.

1. **EGM으로 모호함 없는 설계 완성**
   * `/egm:egm-brainstorm` → `/egm:egm-draft` → `/egm:egm-review` → `/egm:egm-resolve`
   * *(팁: 브레인스토밍 시 "최종 구현은 Ralph Loop로 돌릴 예정이니 작은 단위 태스크 분해와 자동 테스트 기준을 명확히 포함하자"고 명시하면 `egm-implementation-readiness` 리뷰어가 사전에 검증해 줍니다.)*
2. **Ralph 4종 세트로 변환 지시**
   * 설계가 확정되면 같은 대화창(Elephant)에서 아래와 같이 요청합니다:
     > *"확정된 `design_draft.md`를 바탕으로 Ralph Loop를 돌릴 수 있도록 1) `PRD.md` (작은 태스크 체크리스트), 2) `PROMPT.md` (1태스크=1커밋 지시서), 3) `progress.md` (초기 템플릿), 4) 실행/검증 스크립트(`ralph.ps1`)를 만들어줘."*
   * *(빈 프로젝트라면 `PRD.md`의 1번 태스크를 "프로젝트 초기화 및 테스트 러너 세팅"으로 잡아야 첫 루프부터 검증이 정상 동작합니다.)*

---

## 6. Ralph Loop 참고 웹페이지

### 원조 글 & 공식 가이드 (Geoffrey Huntley)
* **원조 블로그 아티클:** https://ghuntley.com/ralph/
* **공식 플레이북 / 가이드 저장소:** https://github.com/ghuntley/how-to-ralph-wiggum

### 대표적인 GitHub 구현체
* **`snarktank/ralph`:** https://github.com/snarktank/ralph *(PRD 체크리스트 + Git 이력 + 상태 파일 기반의 대표적인 구현)*
* **`frankbria/ralph-claude-code`:** https://github.com/frankbria/ralph-claude-code *(지능형 종료 감지 포함)*
* **`Th0rgal/open-ralph-wiggum`:** https://github.com/Th0rgal/open-ralph-wiggum *(다양한 코딩 에이전트 CLI를 감싸는 오픈소스 래퍼)*
* **`agenticloops-ai/ralph-loop`:** https://github.com/agenticloops-ai/ralph-loop *(기본 스캐폴딩 템플릿)*

### Loop Engineering 확장 도구
* **`cobusgreyling/loop-engineering`:** https://github.com/cobusgreyling/loop-engineering
