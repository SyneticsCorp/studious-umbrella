from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

DEFAULT_CHILD_PROBABILITY_THRESHOLD = 0.75
DEFAULT_PET_PROBABILITY_THRESHOLD = 0.75
DEFAULT_HIGH_TEMPERATURE_C = 29.0
DEFAULT_LOW_TEMPERATURE_C = 3.0
DEFAULT_ALERT_COOLDOWN_SECONDS = 300


class SettingsError(ValueError):
    """Raised when safety policy settings are invalid."""


@dataclass(frozen=True, slots=True)
class SafetySettings:
    child_probability_threshold: float = DEFAULT_CHILD_PROBABILITY_THRESHOLD
    pet_probability_threshold: float = DEFAULT_PET_PROBABILITY_THRESHOLD
    high_temperature_c: float = DEFAULT_HIGH_TEMPERATURE_C
    low_temperature_c: float = DEFAULT_LOW_TEMPERATURE_C
    alert_cooldown_seconds: int = DEFAULT_ALERT_COOLDOWN_SECONDS

    @classmethod
    def from_mapping(cls, values: Mapping[str, str]) -> SafetySettings:
        settings = cls(
            child_probability_threshold=_float_setting(
                values, "child_probability_threshold", DEFAULT_CHILD_PROBABILITY_THRESHOLD
            ),
            pet_probability_threshold=_float_setting(
                values, "pet_probability_threshold", DEFAULT_PET_PROBABILITY_THRESHOLD
            ),
            high_temperature_c=_float_setting(
                values, "high_temperature_c", DEFAULT_HIGH_TEMPERATURE_C
            ),
            low_temperature_c=_float_setting(
                values, "low_temperature_c", DEFAULT_LOW_TEMPERATURE_C
            ),
            alert_cooldown_seconds=_int_setting(
                values, "alert_cooldown_seconds", DEFAULT_ALERT_COOLDOWN_SECONDS
            ),
        )
        settings._validate()
        return settings

    def _validate(self) -> None:
        _threshold(self.child_probability_threshold, "child_probability_threshold")
        _threshold(self.pet_probability_threshold, "pet_probability_threshold")
        if self.low_temperature_c >= self.high_temperature_c:
            raise SettingsError("low_temperature_c must be lower than high_temperature_c")
        if self.alert_cooldown_seconds < 1:
            raise SettingsError("alert_cooldown_seconds must be at least 1")


def _float_setting(values: Mapping[str, str], field: str, default: float) -> float:
    raw_value = values.get(field)
    if raw_value is None:
        return default
    try:
        return float(raw_value)
    except ValueError as exc:
        raise SettingsError(f"{field} must be numeric") from exc


def _int_setting(values: Mapping[str, str], field: str, default: int) -> int:
    raw_value = values.get(field)
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError as exc:
        raise SettingsError(f"{field} must be an integer") from exc


def _threshold(value: float, field: str) -> None:
    if not 0.0 < value < 1.0:
        raise SettingsError(f"{field} must be greater than 0 and less than 1")
