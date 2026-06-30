"""Unit tests for ETL pipeline."""

import pytest

from etl.parsers import (
    parse_bool_yn,
    parse_fixed_code,
    parse_float,
    parse_int,
    parse_null,
)


class TestParsers:
    def test_parse_null_empty_string(self):
        assert parse_null("") is None

    def test_parse_null_backslash_n(self):
        assert parse_null("\\N") is None

    def test_parse_null_valid_value(self):
        assert parse_null("NewYork") == "NewYork"

    def test_parse_fixed_code_valid_iata(self):
        assert parse_fixed_code("JFK", 3) == "JFK"

    def test_parse_fixed_code_invalid_length(self):
        assert parse_fixed_code("JFKK", 3) is None

    def test_parse_bool_yn_yes(self):
        assert parse_bool_yn("Y") is True

    def test_parse_bool_yn_no(self):
        assert parse_bool_yn("N") is False

    def test_parse_int_valid(self):
        assert parse_int("42") == 42

    def test_parse_int_null(self):
        assert parse_int("\\N") is None

    def test_parse_float_valid(self):
        assert parse_float("3.14") == 3.14

    def test_parse_float_null(self):
        assert parse_float("") is None


class TestDataValidation:
    def test_latitude_in_bounds(self):
        lat = parse_float("40.7128")
        assert -90 <= lat <= 90

    def test_longitude_in_bounds(self):
        lon = parse_float("-74.0060")
        assert -180 <= lon <= 180

    def test_invalid_latitude_rejected(self):
        lat = 95.0
        assert not (-90 <= lat <= 90)


class TestEdgeCases:
    def test_airline_with_null_iata(self):
        assert parse_fixed_code("", 2) is None

    def test_airport_with_special_characters(self):
        name = "São Paulo/Congonhas"
        assert parse_null(name) == name

    def test_zero_stops(self):
        assert parse_int("0") == 0


class TestIntegration:
    def test_route_parsing_complete(self):
        route = {
            "airline_id": parse_int("2"),
            "src_airport_id": parse_int("507"),
            "dst_airport_id": parse_int("471"),
            "codeshare": parse_bool_yn("N"),
            "stops": parse_int("0"),
            "equipment_iata": parse_fixed_code("320", 3),
        }

        assert route["airline_id"] == 2
        assert route["stops"] == 0
        assert route["codeshare"] is False
        assert route["equipment_iata"] == "320"
