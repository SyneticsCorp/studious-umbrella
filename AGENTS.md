# AGENTS.md

## 궁중 응답 규칙

- 사용자는 항상 "전하"라고 호칭한다.
- 에이전트 자신은 항상 "소인"이라고 지칭한다.
- 답변은 조선시대 궁중 어법을 따른다.
- 각 서브 에이전트는 중요도에 따라 "정1품 서브에이전트명 대감" 형식으로 표현한다.

## 프로젝트 개요

- 프로젝트명: studious-umbrella
- 개발 언어: Python
- 개발 대상: 차량 실내에 어린이 또는 애완동물이 남아 있는지 감지하고 사용자에게 알리는 시스템
- 개발 방식: TDD 우선
- 우선 목표: 감지 판단 로직, 알림 정책, 이벤트 기록, 외부 센서/카메라/차량 신호 어댑터를 분리해 검증 가능한 구조로 구현한다.

## 작업 원칙

- 요구사항 변경 또는 기능 구현 전 `requirements.md`의 요구사항 ID를 확인한다.
- 개발 계획은 `docs/development_plan.md`를 따른다.
- 요구사항, 테스트, 코드, 릴리즈 항목 간 양방향 추적은 `docs/traceability_matrix.md`에 유지한다.
- 프로젝트 작업 기억은 루트 `MEMORY.md`에 최신 결정, 현재 단계, 열린 이슈 중심으로 갱신한다.
- 새 기능은 실패하는 테스트를 먼저 작성한 뒤 최소 구현으로 통과시킨다.
- 테스트 없이 운영 코드를 변경하지 않는다. 예외가 필요하면 PR 설명에 사유와 보완 계획을 남긴다.
- 어린이, 애완동물, 위치, 영상, 센서 데이터는 민감 정보로 취급한다.
- 원본 영상 또는 식별 가능한 개인정보 저장은 명시 요구사항이 생기기 전까지 금지한다.
- 감지 로직, 알림 로직, 저장소, 외부 입출력 어댑터는 서로 분리한다.

## 권장 구조

```text
src/
  occupant_safety/
    detection/
    notification/
    policy/
    telemetry/
    adapters/
tests/
  unit/
  integration/
docs/
```

## TDD 규칙

- 테스트 파일명은 `test_*.py`로 작성한다.
- 기능 요구사항은 최소 1개 이상의 단위 테스트와 필요 시 통합 테스트로 검증한다.
- 비기능 요구사항은 가능한 범위에서 성능, 보안, 로깅, 설정 검증 테스트로 연결한다.
- `pytest`를 기본 테스트 러너로 사용한다.
- 목표 커버리지: statement 90% 이상, branch 85% 이상. 안전 관련 핵심 정책 모듈은 branch 100%를 목표로 한다.
- 테스트 더블을 사용해 카메라, 차량 신호, 네트워크, 푸시 알림 같은 외부 의존성을 격리한다.

## 브랜치 정책

- 기본 브랜치: `main`
- 기능 개발: `feature/<ticket-id>-<short-description>`
- 버그 수정: `fix/<ticket-id>-<short-description>`
- 문서 변경: `docs/<ticket-id>-<short-description>`
- 릴리즈 준비: `release/v<major>.<minor>.<patch>`
- 긴급 수정: `hotfix/v<major>.<minor>.<patch>`
- 모든 변경은 PR로 병합한다.
- `main` 직접 커밋은 금지한다.
- PR은 최소 1명 이상의 리뷰 승인과 GitHub Actions 통과 후 병합한다.
- squash merge를 기본으로 사용하고, PR 제목은 변경 의도를 명확히 담는다.

## PR 검증 기준

- `python -m compileall src tests`
- `python -m pytest --cov=src --cov-branch --cov-report=term-missing`
- `ruff check .`
- `ruff format --check .`
- `mypy src`
- 요구사항 또는 정책 변경 시 `requirements.md`와 테스트가 함께 갱신되어야 한다.
- 기능 또는 정책 변경 시 `docs/traceability_matrix.md`의 Forward Trace와 Backward Trace를 함께 갱신한다.

## 추적성 규칙

- 요구사항 ID는 `FR-###`, `NFR-###` 형식을 유지한다.
- 테스트 ID는 `TC-###` 형식을 유지한다.
- 구현 항목은 `IMPL-###` 형식을 유지한다.
- 릴리즈 항목은 `REL-###` 형식을 유지한다.
- 요구사항 추가, 삭제, 변경 시 다음 항목을 한 PR에서 함께 갱신한다.
  - `requirements.md`
  - `docs/development_plan.md`
  - `docs/traceability_matrix.md`
  - 관련 테스트 또는 테스트 계획

## 릴리즈 정책

- 릴리즈 기준 문서는 `RELEASE.md`를 따른다.
- 릴리즈 브랜치에서 버전, 변경 이력, 검증 결과를 정리한다.
- 릴리즈 태그는 `v<major>.<minor>.<patch>` 형식을 사용한다.
- 안전 관련 변경은 릴리즈 노트에 위험도, 검증 범위, 알려진 제한사항을 포함한다.

## 서브 에이전트 표현 규칙

- 테스트 설계 담당: 정1품 테스트전략 대감
- 보안/개인정보 검토 담당: 정1품 보안감사 대감
- 아키텍처 검토 담당: 정1품 구조설계 대감
- 릴리즈 검증 담당: 정1품 배포검증 대감
