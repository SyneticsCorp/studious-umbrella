# 양방향 추적 매트릭스

## 1. 목적

이 문서는 요구사항, 테스트, 구현 항목, 릴리즈 항목 간 양방향 추적을 확보한다. 개발 중 실제 테스트 파일과 코드 파일이 생기면 `Planned` 항목을 실제 경로로 갱신한다.

## 2. 추적 ID 규칙

| 유형 | 형식 | 예시 |
| --- | --- | --- |
| 기능 요구사항 | `FR-###` | `FR-001` |
| 비기능 요구사항 | `NFR-###` | `NFR-001` |
| 테스트 케이스 | `TC-###` | `TC-001` |
| 구현 항목 | `IMPL-###` | `IMPL-001` |
| 릴리즈 항목 | `REL-###` | `REL-001` |

## 3. Forward Trace: 요구사항에서 검증/구현으로

| Requirement | Tests | Implementation | Release Evidence | Status |
| --- | --- | --- | --- | --- |
| FR-001 | TC-001 | IMPL-001 | REL-001 | Implemented |
| FR-002 | TC-002 | IMPL-002 | REL-001 | Planned |
| FR-003 | TC-003 | IMPL-002 | REL-001 | Planned |
| FR-004 | TC-004 | IMPL-003 | REL-001 | Planned |
| FR-005 | TC-004 | IMPL-003 | REL-001 | Planned |
| FR-006 | TC-005 | IMPL-003 | REL-001 | Planned |
| FR-007 | TC-005 | IMPL-004 | REL-001 | Planned |
| FR-008 | TC-006 | IMPL-005 | REL-001 | Planned |
| FR-009 | TC-011 | IMPL-006 | REL-001 | Planned |
| FR-010 | TC-007 | IMPL-007 | REL-001 | Planned |
| FR-011 | TC-010 | IMPL-008 | REL-001 | Planned |
| FR-012 | TC-012 | IMPL-009 | REL-001 | Implemented |
| FR-013 | TC-008 | IMPL-001 | REL-001 | Implemented |
| FR-014 | TC-013 | IMPL-010 | REL-001 | Planned |
| FR-015 | TC-014 | IMPL-011 | REL-001 | Planned |
| NFR-001 | TC-015 | IMPL-003, IMPL-004 | REL-001 | Planned |
| NFR-002 | TC-016 | IMPL-003 | REL-001 | Planned |
| NFR-003 | TC-009 | IMPL-007 | REL-001 | Planned |
| NFR-004 | TC-009 | IMPL-007 | REL-001 | Planned |
| NFR-005 | TC-010 | IMPL-008 | REL-001 | Planned |
| NFR-006 | TC-001, TC-010 | IMPL-001, IMPL-008 | REL-001 | In Progress |
| NFR-007 | TC-012 | IMPL-009 | REL-001 | Implemented |
| NFR-008 | TC-017 | IMPL-012 | REL-001 | Implemented |
| NFR-009 | TC-017 | IMPL-012 | REL-001 | Implemented |
| NFR-010 | TC-018 | IMPL-012 | REL-001 | Planned |
| NFR-011 | TC-007 | IMPL-007 | REL-001 | Planned |
| NFR-012 | TC-019 | IMPL-012 | REL-001 | Planned |

## 4. Backward Trace: 테스트에서 요구사항으로

| Test | Requirements | Planned Test Location | Status |
| --- | --- | --- | --- |
| TC-001 | FR-001, NFR-006 | `tests/unit/test_detection_event.py` | Implemented |
| TC-002 | FR-002 | `tests/unit/test_occupant_detection_policy.py` | Planned |
| TC-003 | FR-003 | `tests/unit/test_occupant_detection_policy.py` | Planned |
| TC-004 | FR-004, FR-005 | `tests/unit/test_risk_policy.py` | Planned |
| TC-005 | FR-006, FR-007 | `tests/unit/test_notification_policy.py` | Planned |
| TC-006 | FR-008 | `tests/unit/test_notification_policy.py` | Planned |
| TC-007 | FR-010, NFR-011 | `tests/unit/test_audit_logger.py` | Planned |
| TC-008 | FR-013 | `tests/unit/test_detection_event.py` | Implemented |
| TC-009 | NFR-003, NFR-004 | `tests/unit/test_audit_logger.py` | Planned |
| TC-010 | FR-011, NFR-005, NFR-006 | `tests/unit/test_notification_adapter.py` | Planned |
| TC-011 | FR-009 | `tests/unit/test_recipients.py` | Planned |
| TC-012 | FR-012, NFR-007 | `tests/unit/test_settings.py` | Implemented |
| TC-013 | FR-014 | `tests/unit/test_state_query.py` | Planned |
| TC-014 | FR-015 | `tests/integration/test_simulated_alert_flow.py` | Planned |
| TC-015 | NFR-001 | `tests/unit/test_policy_determinism.py` | Planned |
| TC-016 | NFR-002 | `tests/unit/test_risk_policy_performance.py` | Planned |
| TC-017 | NFR-008, NFR-009 | `.github/workflows/pr-validation.yml`, `pyproject.toml`, `tests/unit/test_package_bootstrap.py` | Implemented |
| TC-018 | NFR-010 | PR template or review checklist | Planned |
| TC-019 | NFR-012 | `RELEASE.md` checklist | Planned |

## 5. Backward Trace: 구현에서 요구사항으로

| Implementation | Planned Location | Requirements | Tests | Status |
| --- | --- | --- | --- | --- |
| IMPL-001 | `src/occupant_safety/detection/events.py` | FR-001, FR-013, NFR-006 | TC-001, TC-008 | Implemented |
| IMPL-002 | `src/occupant_safety/detection/policy.py` | FR-002, FR-003 | TC-002, TC-003 | Planned |
| IMPL-003 | `src/occupant_safety/policy/risk.py` | FR-004, FR-005, FR-006, NFR-001, NFR-002 | TC-004, TC-015, TC-016 | Planned |
| IMPL-004 | `src/occupant_safety/policy/notification.py` | FR-007, NFR-001 | TC-005, TC-015 | Planned |
| IMPL-005 | `src/occupant_safety/notification/cooldown.py` | FR-008 | TC-006 | Planned |
| IMPL-006 | `src/occupant_safety/notification/recipients.py` | FR-009 | TC-011 | Planned |
| IMPL-007 | `src/occupant_safety/telemetry/audit.py` | FR-010, NFR-003, NFR-004, NFR-011 | TC-007, TC-009 | Planned |
| IMPL-008 | `src/occupant_safety/adapters/notification.py` | FR-011, NFR-005, NFR-006 | TC-010 | Planned |
| IMPL-009 | `src/occupant_safety/settings.py` | FR-012, NFR-007 | TC-012 | Implemented |
| IMPL-010 | `src/occupant_safety/state.py` | FR-014 | TC-013 | Planned |
| IMPL-011 | `src/occupant_safety/simulation.py` | FR-015 | TC-014 | Planned |
| IMPL-012 | `.github/workflows/pr-validation.yml`, `pyproject.toml`, `src/occupant_safety/__init__.py`, `tests/unit/test_package_bootstrap.py`, `RELEASE.md` | NFR-008, NFR-009, NFR-010, NFR-012 | TC-017, TC-018, TC-019 | In Progress |

## 6. 릴리즈 추적

| Release Evidence | Description | Requirements | Status |
| --- | --- | --- | --- |
| REL-001 | v0.1.0 초기 릴리즈 검증 묶음 | FR-001~FR-015, NFR-001~NFR-012 | Planned |

## 7. 추적 완결성 점검

| 점검 항목 | 현재 상태 |
| --- | --- |
| 모든 기능 요구사항에 테스트 ID가 있는가 | Yes |
| 모든 비기능 요구사항에 테스트 또는 검증 ID가 있는가 | Yes |
| 모든 테스트 ID가 요구사항으로 역추적되는가 | Yes |
| 모든 구현 항목이 요구사항과 테스트로 역추적되는가 | Yes |
| 릴리즈 항목이 요구사항 묶음으로 추적되는가 | Yes |
| 실제 코드 경로가 존재하는가 | Partial, Phase 1 and Phase 2 paths exist; later phase domain paths remain planned |
