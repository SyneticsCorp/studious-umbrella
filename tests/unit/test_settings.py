import pytest

from occupant_safety.settings import SafetySettings, SettingsError


def test_builds_settings_from_mapping() -> None:
    settings = SafetySettings.from_mapping(
        {
            "child_probability_threshold": "0.7",
            "pet_probability_threshold": "0.65",
            "high_temperature_c": "30.0",
            "low_temperature_c": "2.5",
            "alert_cooldown_seconds": "300",
        }
    )

    assert settings.child_probability_threshold == 0.7
    assert settings.pet_probability_threshold == 0.65
    assert settings.high_temperature_c == 30.0
    assert settings.low_temperature_c == 2.5
    assert settings.alert_cooldown_seconds == 300


def test_uses_safe_defaults_when_mapping_is_empty() -> None:
    settings = SafetySettings.from_mapping({})

    assert settings.child_probability_threshold == 0.75
    assert settings.pet_probability_threshold == 0.75
    assert settings.high_temperature_c == 29.0
    assert settings.low_temperature_c == 3.0
    assert settings.alert_cooldown_seconds == 300


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("child_probability_threshold", "0"),
        ("child_probability_threshold", "1.1"),
        ("pet_probability_threshold", "-0.1"),
        ("pet_probability_threshold", "1"),
        ("alert_cooldown_seconds", "0"),
    ],
)
def test_rejects_invalid_settings_values(field: str, value: str) -> None:
    with pytest.raises(SettingsError, match=field):
        SafetySettings.from_mapping({field: value})


def test_rejects_temperature_thresholds_that_are_not_ordered() -> None:
    with pytest.raises(SettingsError, match="low_temperature_c"):
        SafetySettings.from_mapping(
            {
                "high_temperature_c": "5.0",
                "low_temperature_c": "5.0",
            }
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("high_temperature_c", "warm"),
        ("alert_cooldown_seconds", "soon"),
    ],
)
def test_rejects_non_numeric_settings_values(field: str, value: str) -> None:
    with pytest.raises(SettingsError, match=field):
        SafetySettings.from_mapping({field: value})
