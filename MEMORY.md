# MEMORY.md

## 목적

이 파일은 `studious-umbrella` 프로젝트의 저장소-local 작업 기억이다. 작업을 이어받는 소인과 정1품 서브에이전트명 대감들은 이 파일을 먼저 확인해 현재 결정, 진행 단계, 추적 상태를 파악한다.

## 현재 프로젝트 상태

- 저장소: `D:\GitRepo\studious-umbrella`
- 원격 저장소: `https://github.com/SyneticsCorp/studious-umbrella.git`
- 기본 브랜치: `main`
- 개발 언어: Python 3.11 이상
- 개발 방식: TDD 우선
- 주제: 차량 내 어린이 또는 애완동물 감지 및 알림 시스템

## 핵심 문서

- `AGENTS.md`: 작업 규칙, 브랜치 정책, TDD 기준, 추적성 규칙
- `requirements.md`: 기능 요구사항, 비기능 요구사항, 초기 테스트 케이스
- `docs/development_plan.md`: 단계별 개발 계획
- `docs/traceability_matrix.md`: 요구사항, 테스트, 구현, 릴리즈 간 양방향 추적
- `RELEASE.md`: 릴리즈 절차와 릴리즈 노트 양식
- `.github/workflows/pr-validation.yml`: PR 품질 게이트

## 현재 기준 결정

- 실제 카메라 모델 학습, 차량 CAN 통신, 상용 푸시 연동은 초기 범위에서 제외한다.
- 초기 구현은 센서 입력 추상화, 감지 판단 정책, 위험도 산정, 알림 정책, 감사 로그를 우선한다.
- 원본 영상, 음성, 식별 가능한 개인정보 저장은 금지한다.
- 외부 입출력은 어댑터로 분리하고 테스트에서는 가짜 어댑터를 사용한다.
- 모든 기능 변경은 요구사항 ID와 테스트 ID를 함께 남긴다.

## 단계 상태

| Phase | 이름 | 상태 | 기준 문서 |
| --- | --- | --- | --- |
| Phase 0 | 프로젝트 거버넌스 | 완료 | `AGENTS.md`, `requirements.md`, `RELEASE.md`, GitHub Actions |
| Phase 1 | Python 패키지/TDD 기반 | 완료 | `docs/development_plan.md`, `pyproject.toml`, `src/occupant_safety/`, `tests/` |
| Phase 2 | 감지 입력 및 공통 모델 | 완료 | `docs/development_plan.md`, `docs/traceability_matrix.md`, `src/occupant_safety/detection/events.py`, `src/occupant_safety/settings.py` |
| Phase 3 | 위험도 및 알림 정책 | 대기 | `docs/development_plan.md`, `docs/traceability_matrix.md` |
| Phase 4 | 감사 로그와 상태 조회 | 대기 | `docs/development_plan.md`, `docs/traceability_matrix.md` |
| Phase 5 | 통합 시뮬레이션 및 릴리즈 준비 | 대기 | `docs/development_plan.md`, `RELEASE.md` |

## 다음 작업 후보

1. Phase 3 시작 전 어린이/애완동물 감지 및 위험도 정책 Red 테스트 작성
2. Phase 3 최소 구현으로 Green 달성
3. `docs/traceability_matrix.md`에 Phase 3 실제 코드와 테스트 경로 반영

## 최근 검증

- Phase 1 로컬 검증일: 2026-06-05
- 실행 환경: Windows, Python 3.14.3 로컬 인터프리터
- `python -m compileall src tests`: 통과
- `python -m pytest --cov=src --cov-branch --cov-report=term-missing`: 1 passed, coverage 100%
- `python -m ruff check .`: 통과
- `python -m ruff format --check .`: 통과
- `python -m mypy src`: 통과
- 참고: CI는 Python 3.11 및 3.12 매트릭스로 검증한다.

- Phase 2 로컬 검증일: 2026-06-05
- 실행 환경: Windows, Python 3.14.3 로컬 인터프리터
- `python -m compileall src tests`: 통과
- `python -m pytest --cov=src --cov-branch --cov-report=term-missing`: 31 passed, coverage 100%
- `python -m ruff check .`: 통과
- `python -m ruff format --check .`: 통과
- `python -m mypy src`: 통과
- 참고: CI는 Python 3.11 및 3.12 매트릭스로 검증한다.

## 작업 기억 갱신 규칙

- 개발 단계가 완료되면 `단계 상태`를 갱신한다.
- 중요한 설계 결정은 `현재 기준 결정`에 추가한다.
- 막힌 문제는 이 파일에 원인, 재현 명령, 다음 조치를 남긴다.
- 요구사항, 테스트, 코드, 릴리즈 추적이 바뀌면 `docs/traceability_matrix.md`를 우선 갱신하고 이 파일에는 요약만 남긴다.
