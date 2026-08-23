# Mutation Testing 벤치마크 평가 결과 보고서 (Evaluation Report)

## 1. 벤치마크 평가 개요
본 보고서는 Test 작성 전문가 에이전트의 기능 정확성(Functional Correctness) 검증을 위한 Mutation Testing 기반 벤치마크 평가 결과입니다.

- **대상 코드셋**: 6개 모듈 총 30개 순수 함수
- **주입 결함(Mutants)**: 4대 연산자 기반 총 55개 뮤턴트
- **평가 기준**: ISO/IEC 25059 기능 적합성 및 혼동 행렬(Confusion Matrix)

---

## 2. 핵심 평가 결과 요약 (Executive Summary)

```text
[*] Mutation Testing 벤치마크 평가 결과
- Clean Code (TN): 30/30 Pass (100.0%)
- Mutant Killed (TP): 55/55 Killed (100.0%)
- Precision: 100.00% | Recall: 100.00% | F1-Score: 100.00% | Accuracy: 100.00%
- 난이도별: Easy(14/14), Medium(17/17), Hard(9/9), Killer(15/15) Killed
```

---

## 3. 혼동 행렬 (Confusion Matrix)

| 구분 | **결함 주입 코드 (`moresrc`)**<br>*(Actual Positive)* | **정상 원본 코드 (`cleansrc`)**<br>*(Actual Negative)* |
| :--- | :---: | :---: |
| **생성된 TC 실행: Fail (결함 검출)**<br>*(Predicted Positive)* | **True Positive (TP) = 55**<br>*(Mutant Killed / 정상 검출)* | **False Positive (FP) = 0**<br>*(Broken Test / 오탐)* |
| **생성된 TC 실행: Pass (정상 통과)**<br>*(Predicted Negative)* | **False Negative (FN) = 0**<br>*(Mutant Survived / 결함 누락)* | **True Negative (TN) = 30**<br>*(Clean Pass / 정상 통과)* |

---

## 4. 정량 평가 메트릭 (Metrics)

| 메트릭 (Metric) | 산출식 | 측정값 | 목표 수준 | 판정 |
|---|---|:---:|:---:|:---:|
| **Precision (정밀도)** | $\frac{TP}{TP + FP} = \frac{55}{55 + 0}$ | **100.00%** | $\ge 90.0\%$ | **PASS** |
| **Recall (재현율 / Mutation Score)** | $\frac{TP}{TP + FN} = \frac{55}{55 + 0}$ | **100.00%** | $\ge 90.0\%$ | **PASS** |
| **F1-Score (기능 정확성)** | $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ | **100.00%** | $\ge 90.0\%$ | **PASS** |
| **Accuracy (정확도)** | $\frac{TP + TN}{TP + FP + FN + TN}$ | **100.00%** | - | **PASS** |

---

## 5. 다차원 세부 분석

### 5.1 난이도별 분석
| 난이도 | 전체 수 | 검출(Killed) | 누락(Survived) | 검출률 |
|:---:|:---:|:---:|:---:|:---:|
| **Easy** | 14개 | 14개 | 0개 | **100.0%** |
| **Hard** | 9개 | 9개 | 0개 | **100.0%** |
| **Killer** | 15개 | 15개 | 0개 | **100.0%** |
| **Medium** | 17개 | 17개 | 0개 | **100.0%** |

### 5.2 연산자별 분석
| 뮤테이션 연산자 | 전체 수 | 검출(Killed) | 검출률 |
|---|:---:|:---:|:---:|
| `arithmetic_operator` | 9개 | 9개 | **100.0%** |
| `boundary_change` | 28개 | 28개 | **100.0%** |
| `condition_negation` | 8개 | 8개 | **100.0%** |
| `return_value` | 10개 | 10개 | **100.0%** |

### 5.3 모듈별 분석
| 모듈명 | 전체 수 | 검출(Killed) | 검출률 |
|---|:---:|:---:|:---:|
| `dsutil` | 11개 | 11개 | **100.0%** |
| `humanize` | 9개 | 9개 | **100.0%** |
| `iterutils` | 8개 | 8개 | **100.0%** |
| `mathutil` | 9개 | 9개 | **100.0%** |
| `strutil` | 9개 | 9개 | **100.0%** |
| `validators` | 9개 | 9개 | **100.0%** |
