import pytest
from pipeline import WeatherRecord
from pydantic import ValidationError


def test_weather_record_valid():
    record = WeatherRecord(
        time="2026-08-07T09:00",
        temperature=30,
        precipitation_probability=20,
    )

    assert record.temperature == 30
    assert record.precipitation_probability == 20


def test_weather_record_invalid():
    with pytest.raises(ValidationError):
        WeatherRecord(
            time="2026-08-07T09:00",
            temperature=100,
            precipitation_probability=150,
        )