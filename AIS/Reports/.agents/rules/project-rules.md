---
trigger: always_on
---

# AI Specialist 설계 과제 프로젝트 규칙 (Project Rules)

## 1. 기본 원칙 및 역할
- 모든 보고서 및 기술 문서는 **명확성, 논리성, 기술적 타당성**을 갖추어 작성합니다.
- Agent 대화는 한글로 한다.

## 2. 최종 산출물 문서 작성 및 양식 가이드 (/doc-final/AI Specialist 설계 과제보고서.pptx)
- **한국어 표준 및 용어**: 공식 기술 문서/보고서 어조(개조식 문장, 명확한 서술)를 사용합니다.
- 목차 
  - 01. 과제 소개
     . 과제 배경 필요성
     . 과제 개요
  - 02. 요구사항 분석
     . 기능 요구사항 및 제약 사항
     . 품질 요구사항 
  - 03. 설계
     . Architecture Decision (설계 문제 정의, 설계 1안/2안, 설계 결정 및 근거)
     . 최종 Architecture 
     . 유지보수 프로세스
     . AI Governance
  - 04. 구현 및 검증
     . 구현
     . 품질 속성 검증 (품질 요구사항 별 검증 결과, 달성 여부)
     . 결론 (주요 성과, 향후 계획)


## 3. 과제 진행 지침 
- [기능 요구사항] 최소 4개 선정 필수, AI 관련 요구사항이 포함되어야 함
- [품질 요구사항] 품질 속성 최소 4개 이상, 이중 AI 품질 속성에서 2개 이상 반드시 포함
  - AI 품질 속성 : ISO/IEC 25059 기반 품질 속성(Functional Correctness, Robustness, Privacy, Fairness, Performance Efficiency, Functional Adaptability, Controllability, Explainability) 
  - 명확한 측정 방법 시나리오, 정량적 산출식, 목표 수치(Target)을 함께 제시합니다.
- [Architecture Decision] 설계 문제(DP) 2개 이상 작성
- 객체지향 설계에는 SOLID principles를 적용한다.
- 소프트웨어 아키텍처 설계에는 ADD 3.0(Attribute-Driven Design 3.0) 방법론을 적용한다.
- [구현] 데모 시나리오 
- [유지보수 프로세스] AI 모델 및 데이터 Life Cycle 관리 방안, 운영 모니터링 (가드레일 지표) 등
- [AI Governance] 데이터 수집의 적법성, 개인정보 침해, 데이터 편향성 검토, 모델, Compliance 준수 여부 등
- mermaid 를 사용하여 다이어그램을 그린다.
    - 노드 ID와 대괄호 사이 공백 금지 (`NodeID["Label"]`)
    - 라벨 내 줄바꿈 이스케이프 문자(`\n`) 사용 금지 (필요 시 `<br/>` 사용)
    - `graph TD` 플로우차트에서는 `classDiagram` 전용 관계선(`..> Node : Label`) 사용 금지, 플로우차트 화살표 연동 표기법(`-.->|"Label"|`) 사용
    - Sequence Diagram 내 외부 Actor는 `System Boundary Box` 외부에 배치하고, 내부 시스템 파티시펀트만 `box "System Boundary: ..."`로 캡슐화
    - 명확성과 단순함: 너무 많은 정보를 한 번에 담지 말고, 핵심 컴포넌트와 관계(의존성, 상속 등)를 직관적으로 표현하세요.
    - 요약 설명 제공: 다이어그램 출력 전후에 구조의 핵심 의도나 데이터 흐름을 2~3줄로 짧게 설명하세요.
- 상위 산출물(서브시스템 및 컴포넌트 명칭 1:1 일치 등) 일치시켜 하향식 구조적 추적성을 유지한다.