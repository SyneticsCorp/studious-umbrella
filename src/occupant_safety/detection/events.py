from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class DetectionInputError(ValueError):
    """Raised when a sensor payload cannot be normalized into a detection event."""


class SensorSource(StrEnum):
    CAMERA = "camera"
    TEMPERATURE = "temperature"
    WEIGHT = "weight"
    SOUND = "sound"
    VEHICLE = "vehicle"


@dataclass(frozen=True, slots=True)
class DetectionEvent:
    event_id: str
    source: SensorSource
    observed_at: datetime
    child_probability: float
    pet_probability: float
    vehicle_locked: bool
    cabin_temperature_c: float | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> DetectionEvent:
        event_id = _required_str(payload, "event_id")
        source = _parse_source(_required(payload, "source"))
        observed_at = _parse_observed_at(_required(payload, "observed_at"))
        child_probability = _probability(payload.get("child_probability", 0.0), "child_probability")
        pet_probability = _probability(payload.get("pet_probability", 0.0), "pet_probability")
        vehicle_locked = _required_bool(payload, "vehicle_locked")
        cabin_temperature_c = _optional_float(
            payload.get("cabin_temperature_c"), "cabin_temperature_c"
        )

        return cls(
            event_id=event_id,
            source=source,
            observed_at=observed_at,
            child_probability=child_probability,
            pet_probability=pet_probability,
            vehicle_locked=vehicle_locked,
            cabin_temperature_c=cabin_temperature_c,
        )


def _required(payload: Mapping[str, Any], field: str) -> Any:
    if field not in payload:
        raise DetectionInputError(f"{field} is required")
    return payload[field]


def _required_str(payload: Mapping[str, Any], field: str) -> str:
    value = _required(payload, field)
    if not isinstance(value, str) or not value.strip():
        raise DetectionInputError(f"{field} must be a non-empty string")
    return value


def _required_bool(payload: Mapping[str, Any], field: str) -> bool:
    value = _required(payload, field)
    if not isinstance(value, bool):
        raise DetectionInputError(f"{field} must be a boolean")
    return value


def _parse_source(value: Any) -> SensorSource:
    if isinstance(value, SensorSource):
        return value
    if not isinstance(value, str):
        raise DetectionInputError("source must be a string")
    try:
        return SensorSource(value)
    except ValueError as exc:
        raise DetectionInputError(f"source is not supported: {value}") from exc


def _parse_observed_at(value: Any) -> datetime:
    if isinstance(value, datetime):
        observed_at = value
    elif isinstance(value, str):
        try:
            observed_at = datetime.fromisoformat(value)
        except ValueError as exc:
            raise DetectionInputError("observed_at must be ISO 8601 datetime") from exc
    else:
        raise DetectionInputError("observed_at must be datetime or ISO 8601 string")

    if observed_at.tzinfo is None or observed_at.utcoffset() is None:
        raise DetectionInputError("observed_at must include timezone")
    return observed_at


def _probability(value: Any, field: str) -> float:
    parsed = _optional_float(value, field)
    if parsed is None or not 0.0 <= parsed <= 1.0:
        raise DetectionInputError(f"{field} must be between 0 and 1")
    return parsed


def _optional_float(value: Any, field: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise DetectionInputError(f"{field} must be numeric")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise DetectionInputError(f"{field} must be numeric") from exc
