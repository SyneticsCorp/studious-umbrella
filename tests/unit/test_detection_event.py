from datetime import UTC, datetime

import pytest

from occupant_safety.detection.events import DetectionEvent, DetectionInputError, SensorSource


def test_builds_common_detection_event_from_camera_payload() -> None:
    event = DetectionEvent.from_payload(
        {
            "event_id": "evt-001",
            "source": "camera",
            "observed_at": "2026-06-05T12:00:00+09:00",
            "child_probability": 0.82,
            "pet_probability": 0.21,
            "cabin_temperature_c": 31.5,
            "vehicle_locked": True,
        }
    )

    assert event.event_id == "evt-001"
    assert event.source is SensorSource.CAMERA
    assert event.child_probability == 0.82
    assert event.pet_probability == 0.21
    assert event.cabin_temperature_c == 31.5
    assert event.vehicle_locked is True


def test_accepts_datetime_observation_time_for_testable_adapters() -> None:
    observed_at = datetime(2026, 6, 5, 3, 0, tzinfo=UTC)

    event = DetectionEvent.from_payload(
        {
            "event_id": "evt-002",
            "source": SensorSource.WEIGHT,
            "observed_at": observed_at,
            "child_probability": 0.1,
            "pet_probability": 0.0,
            "vehicle_locked": False,
        }
    )

    assert event.observed_at == observed_at
    assert event.source is SensorSource.WEIGHT


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("child_probability", -0.01),
        ("child_probability", 1.01),
        ("pet_probability", -0.01),
        ("pet_probability", 1.01),
    ],
)
def test_rejects_probability_outside_unit_interval(field: str, value: float) -> None:
    payload = {
        "event_id": "evt-003",
        "source": "camera",
        "observed_at": "2026-06-05T12:00:00+09:00",
        "child_probability": 0.4,
        "pet_probability": 0.3,
        "vehicle_locked": False,
    }
    payload[field] = value

    with pytest.raises(DetectionInputError, match=field):
        DetectionEvent.from_payload(payload)


@pytest.mark.parametrize("missing_field", ["event_id", "source", "observed_at", "vehicle_locked"])
def test_rejects_missing_required_fields(missing_field: str) -> None:
    payload = {
        "event_id": "evt-004",
        "source": "camera",
        "observed_at": "2026-06-05T12:00:00+09:00",
        "child_probability": 0.4,
        "pet_probability": 0.3,
        "vehicle_locked": False,
    }
    payload.pop(missing_field)

    with pytest.raises(DetectionInputError, match=missing_field):
        DetectionEvent.from_payload(payload)


def test_rejects_empty_event_id() -> None:
    with pytest.raises(DetectionInputError, match="event_id"):
        DetectionEvent.from_payload(
            {
                "event_id": " ",
                "source": "camera",
                "observed_at": "2026-06-05T12:00:00+09:00",
                "vehicle_locked": False,
            }
        )


@pytest.mark.parametrize("source", [42, "radar"])
def test_rejects_unsupported_source(source: object) -> None:
    with pytest.raises(DetectionInputError, match="source"):
        DetectionEvent.from_payload(
            {
                "event_id": "evt-005",
                "source": source,
                "observed_at": "2026-06-05T12:00:00+09:00",
                "vehicle_locked": False,
            }
        )


def test_rejects_non_boolean_vehicle_locked() -> None:
    with pytest.raises(DetectionInputError, match="vehicle_locked"):
        DetectionEvent.from_payload(
            {
                "event_id": "evt-006",
                "source": "camera",
                "observed_at": "2026-06-05T12:00:00+09:00",
                "vehicle_locked": "false",
            }
        )


def test_rejects_naive_observation_time() -> None:
    with pytest.raises(DetectionInputError, match="observed_at"):
        DetectionEvent.from_payload(
            {
                "event_id": "evt-007",
                "source": "camera",
                "observed_at": "2026-06-05T12:00:00",
                "child_probability": 0.4,
                "pet_probability": 0.3,
                "vehicle_locked": False,
            }
        )


@pytest.mark.parametrize("observed_at", ["not-a-date", 123])
def test_rejects_invalid_observation_time(observed_at: object) -> None:
    with pytest.raises(DetectionInputError, match="observed_at"):
        DetectionEvent.from_payload(
            {
                "event_id": "evt-008",
                "source": "camera",
                "observed_at": observed_at,
                "vehicle_locked": False,
            }
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("child_probability", None),
        ("pet_probability", True),
        ("cabin_temperature_c", object()),
    ],
)
def test_rejects_non_numeric_probability_or_temperature(field: str, value: object) -> None:
    payload = {
        "event_id": "evt-009",
        "source": "camera",
        "observed_at": "2026-06-05T12:00:00+09:00",
        "vehicle_locked": False,
    }
    payload[field] = value

    with pytest.raises(DetectionInputError, match=field):
        DetectionEvent.from_payload(payload)
