# 전통적 SW 아키텍처 스타일, 디자인 패턴 및 전술 폴더 파일별 핵심 요약 레퍼런스

> 본 문서는 `reference/전통적SW_ArchitectureStyle_DesignPattern_Tactic/` 폴더 내에 위치한 3개 문서의 원본 목차와 핵심 내용을 문서별로 충실하게 정리한 요약 레퍼런스입니다.

---

## 1. [문서 1] (이론) SW Architecture 설계.pdf 요약

> **문서 분량**: 총 634페이지의 소프트웨어 아키텍처 종합 이론 교재  
> **핵심 주제**: 아키텍처 기본 개념 $\rightarrow$ 아키텍처 스타일 $\rightarrow$ 아키텍처 문서화(View Model) $\rightarrow$ 품질 속성 전술(Tactics) $\rightarrow$ 아키텍처 설계 프로세스

### 1.1 Architecture Fundamentals (아키텍처 기초 및 구조)
- **소프트웨어 아키텍처의 정의**: 소프트웨어 시스템의 구조(Structure)로서, 소프트웨어 요소(Elements), 요소들 간의 관계(Relations), 그리고 둘 모두의 속성(Properties)으로 구성됨.
- **아키텍처의 3대 구조 범주 (Structures)**:
  1. **Module Structures**: 시스템을 구현 코드 단위(패키지, 클래스, 레이어)로 분할한 정적 구조.
  2. **Component-and-Connector (C&C) Structures**: 시스템 실행 시(Runtime) 동작하는 컴포넌트와 그들 간의 통신/상호작용 커넥터 구조.
  3. **Allocation Structures**: 소프트웨어 요소가 하드웨어, 네트워크, 파일시스템, 개발 팀 등 비소프트웨어 환경에 매핑되는 물리적/조직적 구조.

---

### 1.2 Architecture Styles (아키텍처 스타일 분류 및 상세)
아키텍처 스타일은 패밀리 시스템의 구조적 패턴을 정의하는 어휘(Elements)와 제약조건(Constraints)의 집합입니다.

#### ① Data Flow Architecture (데이터 흐름 아키텍처)
- **Batch Sequential Style**: 각 단계가 전체 데이터셋을 일괄 처리한 후 다음 단계로 넘기는 구조. 단계 간 종속성이 크고 인터랙티브 처리에 부적합.
- **Pipe-and-Filter Style**:
  - **구성 요소**: Filter(독립적 데이터 변환기), Pipe(단방향 데이터 전송 통로).
  - **특징**: 필터 간의 완전한 독립성 및 결합도 분리, 필터 교체 및 재조합 용이(Modifiability), 점진적 스트림 처리 및 병렬성(Concurrency).

#### ② Data-Centered Architecture (데이터 중심 아키텍처)
- **Repository Style**: 모든 클라이언트 컴포넌트가 중앙 집중식 데이터베이스/저장소를 공유하며 직접 접근. 데이터 공유 효율성은 높으나 저장소 스키마 변경 시 전체 파급.
- **Blackboard Style (칠판 스타일)**:
  - **구성 요소**: Blackboard(공유 작업 데이터 공간), Knowledge Sources(독립적 전문 분석 모듈), Controller(트리거 및 실행 순서 제어기).
  - **특징**: 결정론적 해법이 없는 복잡한 문제(음성 인식, 신호 분석, 복합 AI 추론)를 다수의 지식 소스가 점진적·협력적으로 해결.

#### ③ Hierarchical Architecture (계층형 아키텍처)
- **Main-Subroutine Style**: 메인 프로그램이 서브루틴을 순차/조건부로 호출하는 전통적 절차적 구조.
- **Master-Slave Style**: Master가 작업을 분할하여 복수의 Slave에게 분배하고 결과를 취합. 병렬 처리(Performance)와 복제를 통한 결함 감내(Fault Tolerance) 지원.
- **Layered Architecture Style (계층화 스타일)**:
  - 시스템을 수직 계층으로 분할하여 상위 계층이 하위 계층 서비스를 호출.
  - Strict Layering(인접 계층만 호출) vs Relaxed Layering(건너뛰기 허용).
  - 관심사 분리(Separation of Concerns), 높은 변경용이성(Modifiability) 제공.

#### ④ Interaction-Oriented Architecture (인터랙션 지향 아키텍처)
- **Model-View-Controller (MVC) Style**:
  - **Model**: 비즈니스 데이터 및 핵심 규칙.
  - **View**: 사용자 인터페이스 화면 표현.
  - **Controller**: 사용자 입력을 받아 모델을 갱신하고 적절한 뷰를 선택.
  - 장점: 동일 모델에 대한 다중 뷰 지원 및 UI와 비즈니스 로직의 독립적 변경.
- **Presentation-Abstraction-Control (PAC) Style**: 시스템을 계층적 트리 구조의 자율적 PAC 에이전트로 분할하여 복잡한 다중 에이전트 대화형 UI 지원.

#### ⑤ Distributed Architecture (분산 아키텍처)
- **Client-Server Style**: 명확한 역할 분담(서비스 요청자 vs 제공자), 서버 집중식 데이터 관리.
- **Multi-Tiers Style (3-Tier)**: 논리 계층을 물리적으로 클라이언트 단말, 애플리케이션 서버, 데이터베이스 서버로 분리 배포하여 확장성 및 보안 경계 확보.
- **Broker Style (브로커 스타일)**:
  - 분산 환경에서 클라이언트와 원격 서버 간의 상호작용을 중개자(Broker)가 전담.
  - 서비스 등록(Registry), 위치 투명성(Location Transparency), 메시지 마샬링 처리.
  - 장점: 서버의 동적 추가/교체 용이, 이기종 플랫폼 연동(Interoperability).

---

### 1.3 Documenting Architecture (아키텍처 문서화: SEI View Model)
- **Module Views**: 코드 단위 구조 문서화 (Decomposition Style, Uses Style, Layered Style).
- **C&C Views (Component & Connector)**: 런타임 엔터티 및 통신 채널 문서화 (Pipe-and-Filter, Shared Data, Client-Server, Publish-Subscribe 등).
- **Allocation Views**: 소프트웨어의 물리적 환경 매핑 문서화 (Deployment View, Implementation View, Work Assignment View).

---

### 1.4 Architectural Tactics (품질 속성별 아키텍처 전술 상세)
아키텍처 전술은 시스템의 특정 품질 속성(QA)을 직접 제어하고 만족시키기 위해 아키텍트가 적용하는 기본 메커니즘입니다.

#### [QA 1] Availability Tactics (가용성 전술)
- **결함 감지 (Fault Detection)**:
  - *Ping / Echo*: 주기적 질의를 통해 상대 노드의 정상 동작 및 지연 감시.
  - *Heartbeat*: 피감시 노드가 주기적으로 능동적 생존 신호(비트) 전송.
  - *Exception Detection*: 타임아웃, 널 포인터, 시스템 예외 트랩.
- **결함 복구: 준비 및 수리 (Preparation and Repair)**:
  - *Active Redundancy (Hot Spare)*: 복제본이 동일 요청을 동시에 병렬 처리하여 무중단 절체.
  - *Passive Redundancy (Warm Spare)*: 대기 노드가 주기적으로 상태만 동기화하다가 장애 시 승격.
  - *Cold Spare*: 장애 발생 시 백업 인스턴스 기동 및 복구.
  - *Graceful Degradation*: 비핵심 기능을 일시 차단하고 핵심 기능만 유지.
- **결함 복구: 재도입 (Reintroduction)**:
  - *Shadow Mode*: 복구된 노드를 실제 트래픽에 노출하기 전 섀도우 검증.
  - *State Resynchronization*: 주 노드로부터 최신 상태 및 트랜잭션 로그 동기화.
  - *Rollback*: 이전의 안정적인 체크포인트 상태로 복원.
- **결함 방지 (Fault Prevention)**:
  - *Removal from Service*: 오류 빈도가 높아진 노드를 선제 격리.
  - *Transactions*: ACID 보장을 통한 상태 불일치 방지.
  - *Process Monitor*: 크래시된 프로세스의 자동 재시작 감시.

#### [QA 2] Modifiability Tactics (변경용이성 전술)
- **모듈 크기 축소 (Reduce Module Size)**: *Split Module* (단일 책임 원칙에 따라 분할).
- **응집도 향상 (Increase Cohesion)**: *Increase Semantic Coherence* (관련된 책임만 결집).
- **결합도 감소 (Reduce Coupling)**:
  - *Encapsulate*: 세부 구현을 인터페이스 뒤로 은닉.
  - *Use an Intermediary*: 중개자(Broker, Event Bus, Gateway)를 배치하여 직접 의존 제거.
  - *Restrict Dependencies*: 아키텍처 계층 규칙 준수 (상위 $\rightarrow$ 하위 단방향 참조).
  - *Abstract Common Services*: 로깅, 보안 등 공통 기능을 별도 서비스로 추상화.
- **바인딩 시점 지연 (Defer Binding Time)**:
  - *Runtime Configuration*: 설정 파일(Config)을 통한 런타임 파라미터 제어.
  - *Plugin / Dynamic Load*: 빌드 없이 런타임에 동적으로 모듈/플러그인 바인딩.

#### [QA 3] Performance Tactics (성능 전술)
- **자원 수요 제어 (Control Resource Demand)**:
  - *Manage Sampling Rate*: 센서나 이벤트 유입 주기를 조절하여 부하 제어.
  - *Limit Event Response*: 이벤트 디바운싱(Debounce) 및 스로틀링(Throttle).
  - *Prioritize Events*: 중요도 기반 우선순위 큐(Priority Queue) 적용.
  - *Reduce Overhead*: 직렬화 최소화, 중개 계층 제거, 불필요한 로깅 축소.
  - *Bound Execution Times*: 실행 시간 상한선(Timeout) 강제.
- **자원 관리 (Manage Resources)**:
  - *Increase Resources*: CPU, GPU, 메모리 하드웨어 스케일업.
  - *Introduce Concurrency*: 스레드 풀, 병렬 처리를 통한 다중 코어 활용.
  - *Maintain Multiple Copies (Caching)*: 자주 조회되는 연산 결과를 인메모리에 캐싱.
  - *Bound Queue Sizes*: 큐 크기 제한을 통한 메모리 고갈 방지 및 배압(Backpressure) 제어.
  - *Schedule Resources*: FIFO, Round Robin, EDF 등 최적 스케줄링 기법 적용.

#### [QA 4] Security Tactics (보안 전술)
- **공격 감지 (Detect Attacks)**: *Detect Intrusion (침입 탐지)*, *Verify Message Integrity (무결성 검증 - 해시/서명)*, *Detect Service Denial (DoS 감지)*.
- **공격 저항 (Resist Attacks)**: *Authenticate Actors (인증)*, *Authorize Actors (인가/권한 제어)*, *Encrypt Data (암호화)*, *Limit Exposure (공개 인터페이스/포트 최소화)*.
- **공격 대응 (React to Attacks)**: *Revoke Access (접근 즉각 무효화)*, *Lockout (계정 임시 잠금)*.
- **공격 복구 (Recover from Attacks)**: *Audit Trail (감사 추적 로그)*, *Restore from Backup*.

#### [QA 5] Testability Tactics (시험성 전술)
- **상태 제어 및 관찰 (Control and Observe System State)**:
  - *Specialized Interfaces*: 내부 상태를 직접 조회하고 테스트 입력을 주입하는 전용 인터페이스.
  - *Record / Playback*: 실제 운영 트래픽을 기록하여 테스트 환경에서 동일 재현.
  - *Abstract Data Sources*: 외부 시스템 및 DB를 Mock/Stub으로 교체 가능케 추상화.
  - *Sandbox*: 실제 환경 격리 가상 테스트 공간.
- **복잡도 제한 (Limit Complexity)**:
  - *Limit Structural Complexity*: 순환 참조 제거, 결합도 최소화.
  - *Limit Non-determinism*: 난수 시드 고정, 시간 모의(Mocking)를 통한 결정론적 테스트 보장.

#### [QA 6] Interoperability Tactics (상호운용성 전술)
- **위치 식별 (Locate)**: *Discover Service (서비스 디스커버리)*.
- **인터페이스 관리 (Manage Interfaces)**:
  - *Orchestrate*: 워크플로우 엔진이 복수 시스템의 호출 순서 지휘.
  - *Mediate*: 프로토콜 및 데이터 포맷 중재 변환.
  - *Adapt (Adapter Pattern)*: 비표준 인터페이스를 표준 인터페이스로 적응.

#### [QA 7] Usability Tactics (사용성 전술)
- **사용자 주도 지원 (Support User Initiative)**: *Cancel (진행 작업 취소)*, *Undo (작업 되돌리기)*, *Pause / Resume (일시 정지 및 재개)*, *Aggregate (다중 데이터 취합 표시)*.
- **시스템 주도 지원 (Support System Initiative)**: 사용자 행동 패턴 모델링, 사전 안내 및 자동완성.

---

## 2. [문서 2] AA-DP-5-PatternSummary.docx 요약

> **주제**: GoF 23 디자인 패턴을 "앞으로 일어날 시스템 변화에 어떻게 유연하게 대처할 것인가?"라는 **6대 변경 드라이버(Change Drivers)** 관점으로 체계화한 핵심 요약본

### 2.1 19.1 Designing for Change (변화에 적응하기 쉬운 디자인: 행위/상태 변화 캡슐화)
- **핵심 문제**: 비즈니스 동작 방식이나 정책이 자주 변경될 때, 이를 조건문(if-else)으로 클래스 내부에 하드코딩하면 클래스 전체가 비대해지고 코드 수정의 파급력이 커짐.
- **해결 패턴**:
  - **Strategy (전략 패턴)**: 자주 변할 수 있는 행위(예: 비행 동작 `fly behavior`, 결제 수단)를 별도의 인터페이스로 캡슐화하고 객체 합성을 통해 위임(Delegation). 알고리즘 변종이 나타나더라도 클라이언트 클래스에 미치는 영향 격리.
  - **State (상태 패턴)**: 객체의 내부 상태 변화에 따라 행동이 달라질 때, 상태 자체를 객체화하여 상태 전이 로직을 캡슐화.

### 2.2 19.2 특정 Class 명시해서 객체 생성 안하게 (Object Creation Decoupling)
- **핵심 문제**: 클라이언트 코드 내에서 `new ConcreteClass()`를 직접 호출하면 특정 구체 클래스에 강력하게 결합되어 구현체 교체나 확장이 불가능해짐.
- **해결 패턴**:
  - **Abstract Factory (추상 팩토리 패턴)**: 클라이언트가 `AbstractProductA`, `AbstractProductB`, `AbstractFactory` 인터페이스 수준에서만 프로그래밍하도록 하여, 구체적인 팩토리와 제품군 생성을 완벽히 은닉.
  - **Factory Method (팩토리 메서드 패턴)**: 상속 구조를 활용하여 객체 생성 인터페이스는 상위 프레임워크 클래스에 두고, 구체적인 생성 인스턴스는 하위 클래스가 오버라이딩하여 결정.
  - **Builder (빌더 패턴)**: 복잡한 복합 객체의 생성 알고리즘(파트 생성 및 조립)을 `Director`와 `Builder`로 분리.
  - **Prototype (프로토타입 패턴)**: 복잡한 생성 과정 대신 기존 원본 객체의 복제(Clone)를 통해 새 객체 생성.

### 2.3 19.3 Platform Dependency 없도록 (플랫폼/인프라 의존성 격리)
- **핵심 문제**: OS, UI 위젯, 특정 하드웨어 등 플랫폼 종속적인 코드가 비즈니스 로직과 결합되면 다른 플랫폼으로 이식할 때 시스템 전체를 다시 작성해야 함.
- **해결 패턴**:
  - **Bridge (가교 패턴)**: **기능의 추상화 계층(Abstraction Hierarchy)**과 **플랫폼별 구현 계층(Implementation Hierarchy)**을 두 개의 독립된 클래스 계층으로 분리하여, 서로 독립적으로 진화·확장할 수 있도록 브릿지(위임) 연결.

### 2.4 19.4 Algorithm Dependency 없도록 (알고리즘 변화 격리)
- **핵심 문제**: 전체 작업 흐름의 골격은 일정한데 특정 계산 알고리즘이나 세부 단계만 변경될 때 클라이언트가 영향을 받지 않아야 함.
- **해결 패턴**:
  - **Template Method (템플릿 메서드 패턴)**: 상위 클래스에서 알고리즘의 골격(전체 뼈대 흐름)을 정의하고, 변경이 필요한 특정 스텝만 하위 클래스가 구현(상속 기반).
  - **Strategy (전략 패턴)**: 알고리즘 전체를 독립된 클래스로 캡슐화하여 런타임에 동적으로 갈아 끼움(위임 기반).

### 2.5 19.5 Subclassing만으로 클래스 수 폭발 없도록 (상속의 한계 극복)
- **핵심 문제**: 다양한 부가 기능(스크롤바, 테두리, 암호화, 압축 등)의 조합을 서브클래싱(상속)으로만 구현하면 조합 수만큼 클래스가 기하급수적으로 폭발($2^N$)함.
- **해결 패턴**:
  - **Decorator (데코레이터 패턴)**: 기본 객체와 동일한 인터페이스를 유지하면서 객체를 감싸는(Wrapping) 방식으로 런타임에 유연하게 책임을 동적으로 덧붙임.
  - **Composite (복합체 패턴)**: 단일 객체(Leaf)와 복합 객체(Composite)를 동일한 인터페이스로 처리하여 트리 구조를 단순화.

### 2.6 19.6 기존 클래스 변경 없이 새로운 기능 추가 / 인터페이스 조정
- **핵심 문제**: 기존 레거시나 서드파티 라이브러리 소스코드를 직접 수정할 수 없거나 수정하고 싶지 않은 상황에서 인터페이스를 맞추거나 새 기능을 부여해야 함.
- **해결 패턴**:
  - **Adapter (적응자 패턴)**: 기존 클래스의 인터페이스를 클라이언트가 기대하는 규격으로 변환하여 호환되지 않는 인터페이스 간의 협업 지원.
  - **Facade (퍼사드 패턴)**: 복잡한 다수의 서브시스템 클래스들에 대해 단순하고 통합된 고수준 진입점(창구) 인터페이스 제공.
  - **Proxy (프록시 패턴)**: 대상 객체로의 접근을 제어하거나 지연 로딩(Lazy Initialization), 보안 검사, 로깅을 대행하는 대리자 객체 제공.
  - **Visitor (방문자 패턴)**: 클래스 구조를 변경하지 않고도 데이터 요소들에 적용할 새로운 연산(기능)을 외부 방문자 객체에 캡슐화.

---

## 3. [문서 3] E3_1_1 Architecture Style별 특징 정리.pptx 요약

> **파일 상태 및 내용 안내**: 해당 파일은 원본이 HTML 형식으로 저장되어 있으나, 강의 커리큘럼상 **Architecture Style별 카테고리와 특성을 1장으로 요약·대조하는 매트릭스 자료**입니다. 위 PDF 교재의 스타일 체계와 완벽히 대응됩니다.

### 3.1 Architecture Style 카테고리별 핵심 비교표
| 카테고리 | 대표 스타일 | 주요 구성 컴포넌트 | 주요 커넥터 (연결자) | 핵심 장점 | 핵심 단점 및 트레이드오프 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Data Flow** | **Pipe-and-Filter** | Filter (데이터 변환기) | Pipe (데이터 스트림) | 모듈 독립성, 재조합 용이, 병렬 처리 | 인터랙티브 UI 부적합, 직렬화 오버헤드 |
| **Data-Centered** | **Blackboard** | Blackboard, Knowledge Sources | 제어 통지, 공유 읽기/쓰기 | 복잡·비결정론적 문제 해결, 지식 확장성 | 칠판 스키마 변경 시 전체 파급, 동기화 병목 |
| | **Repository** | 중앙 DB, 접근 클라이언트 | SQL, Direct Access | 데이터 공유 효율성, 무결성 제어 | 중앙 저장소 단일 장애점(SPOF), 병목 |
| **Hierarchical** | **Layered** | Layers (계층별 모듈) | 계층 간 함수 호출 | 관심사 분리, 결합도 감소, 유지보수 | 다계층 통과 오버헤드로 인한 성능 저하 |
| | **Master-Slave** | Master, Slaves | 작업 분배 및 결과 취합 | 병렬 처리(성능), 결함 내성 | Master 단일 장애점, 통신 오버헤드 |
| **Distributed** | **Broker** | Client, Server, Broker, Proxy | RPC, 네트워크 메시징 | 분산 투명성, 컴포넌트 동적 교체 | 브로커 병목 및 경유 지연 시간 |
| | **Client-Server** | Client, Server | 네트워크 프로토콜 (HTTP 등) | 중앙 집중식 관리 및 보안 | 서버 부하 집중, 단일 장애점 |
| **Interaction** | **MVC** | Model, View, Controller | 이벤트 알림, 메서드 호출 | UI와 비즈니스 로직 분리, 다중 뷰 지원 | 단순 애플리케이션에는 과도한 복잡성 |
