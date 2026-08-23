# Mutation Testing Benchmark for Test Agent Evaluation

## 개요
Test 작성 에이전트의 품질을 정량 평가하기 위한 벤치마크 코드셋입니다.

- **Clean Code**: 30개 순수 함수 (6개 모듈)
- **Mutated Code**: 40개 수동 뮤턴트 (4가지 뮤테이션 연산자)
- **Ground Truth**: 뮤턴트별 메타데이터 및 killing input
- **평가 메트릭**: Precision, Recall, F1-Score (Confusion Matrix 기반)

## 코드 구성

### Clean Code (`clean/`)
| 모듈 | 출처 | 함수 수 |
|---|---|---|
| `mathutil.py` | 자체 작성 | 5 |
| `strutil.py` | 자체 작성 | 5 |
| `dsutil.py` | 자체 작성 | 5 |
| `validators.py` | validators 라이브러리 참조 (MIT) | 5 |
| `humanize.py` | humanize 라이브러리 참조 (MIT) | 5 |
| `iterutils.py` | more-itertools/boltons 참조 (MIT) | 5 |

### Mutated Code (`moresrc/`)
- **총 55개 뮤턴트 (표준 40개 + 초고난도 Killer 15개)**
- **난이도 분포**: Easy 14개, Medium 17개, Hard 9개, **Killer 15개**
- **연산자 분포**:
  - 경계값 변경 (Boundary Mutation): 28개
  - 반환값 변경 (Return Value): 10개
  - 산술 변조 (Arithmetic Operator): 9개
  - 조건 반전 (Condition Negation): 8개

---

## 📊 평가 체계: 혼동 행렬 (Confusion Matrix) & 메트릭

Test 작성 에이전트가 생성한 단위 테스트(TC)의 품질을 아래 기준으로 정량 평가합니다.

| 구분 | **결함 주입 코드 (`mutated`)**<br>*(Actual Positive)* | **정상 원본 코드 (`clean`)**<br>*(Actual Negative)* |
| :--- | :--- | :--- |
| **생성된 TC 실행: Fail (결함 검출)**<br>*(Predicted Positive)* | **True Positive (TP)**<br>• 주입된 결함을 감지하여 TC Fail 발생<br>• **Mutant Killed** (정상 검출) | **False Positive (FP)**<br>• 결함 없는 정상 코드인데 TC 오류로 Fail<br>• **Broken/Flaky Test** (오탐) |
| **생성된 TC 실행: Pass (정상 통과)**<br>*(Predicted Negative)* | **False Negative (FN)**<br>• 결함이 주입되었으나 TC가 감지 못하고 Pass<br>• **Mutant Survived** (미탐/결함 누락) | **True Negative (TN)**<br>• 정상 코드에 대해 정상적으로 TC Pass 통과<br>• **Clean Test Pass** (정상 통과) |

### 📈 산출 메트릭

- **Precision (정밀도)**: $\text{Precision} = \frac{TP}{TP + FP}$
  - TC가 Fail을 냈을 때, 실제로 결함이 존재했던 비율 (정상 코드 오탐 방지 지표)
- **Recall (재현율 / Mutation Score)**: $\text{Recall} = \frac{TP}{TP + FN}$
  - 주입된 전체 결함 중 TC가 Fail로 잡아낸 비율 (결함 검출력 지표)
- **F1-Score (종합 기능 정확성)**: $\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$
  - 정밀도와 재현율의 조화평균 (목표: 90.0% 이상)

---

## 사용법

### 1. 환경 설정
```bash
pip install -r requirements.txt
```

### 2. 참조 TC 실행 (벤치마크 정합성 검증)
```bash
pytest tests/test_reference.py -v
```

### 3. 자동 평가 실행
```bash
python run_evaluation.py
```

### 4. 에이전트 생성 TC 평가
```bash
python run_evaluation.py --test-dir <agent_test_dir>
```

### 5. mutmut 자동 뮤턴트 생성 (Phase 2)
```bash
pip install mutmut
mutmut run --paths-to-mutate=clean/ --tests-dir=tests/
mutmut results
```

## 학술 참조
- **Defects4J**: Just et al., ISSTA 2014 — 결함 DB 기반 벤치마크 표준
- **BugsInPy**: Widyasari et al., 2020 — Python 실제 버그 DB
- **MutPy**: Derezińska & Hałas, 2014 — AST 기반 Python 뮤테이션
- **mutmut**: github.com/boxed/mutmut — 실무 Python 뮤테이션 도구
- **validators**: github.com/python-validators — 입력 검증 로직 출처
- **humanize**: github.com/jmoiron/humanize — 사람 친화 포맷팅 출처
- **more-itertools**: github.com/more-itertools — 이터레이터 유틸 출처
