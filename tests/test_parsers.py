import pytest

from streamstats.errors import (
    InvalidEventError,
    InvalidTimestampError,
    UnsupportedFormatError,
)
from streamstats.models import Level
from streamstats.parsers import get_parser, parse_csv, parse_jsonl


def test_parse_csv(tmp_path):
    """Тестирует чтение валидного CSV-файла."""
    file = tmp_path / "test.csv"
    file.write_text(
        "timestamp,level,source,message\n2024-01-01T10:00:00,INFO,app,Start\n"
    )

    events = list(parse_csv(file))

    assert len(events) == 1
    assert events[0].level == Level.INFO
    assert events[0].source == "app"


def test_parse_jsonl(tmp_path):
    """Тестирует чтение валидного JSONL-файла."""
    file = tmp_path / "test.jsonl"
    file.write_text(
        '{"timestamp": "2024-01-01T10:00:00", "level": "ERROR", "source": "db", "message": "Fail"}\n'
    )

    events = list(parse_jsonl(file))

    assert len(events) == 1
    assert events[0].level == Level.ERROR
    assert events[0].message == "Fail"


def test_empty_csv(tmp_path):
    """Тестирует чтение пустого CSV-файла."""
    file = tmp_path / "empty.csv"
    file.write_text("timestamp,level,source,message\n")

    events = list(parse_csv(file))

    assert len(events) == 0


def test_empty_jsonl(tmp_path):
    """Тестирует чтение пустого JSONL-файла."""
    file = tmp_path / "empty.jsonl"
    file.write_text("")

    events = list(parse_jsonl(file))

    assert len(events) == 0


def test_invalid_json(tmp_path):
    """Тестирует обработку невалидного JSON в JSONL."""
    file = tmp_path / "broken.jsonl"
    file.write_text(
        '{"timestamp": "2024-01-01T10:00:00", "level": "INFO", "source": "app", "message": "OK"}\nnot valid json\n'
    )

    with pytest.raises(InvalidEventError) as exc_info:
        list(parse_jsonl(file))

    assert "line 2" in str(exc_info.value)


def test_invalid_timestamp(tmp_path):
    """Тестирует обработку неверной даты."""
    file = tmp_path / "bad_date.csv"
    file.write_text("timestamp,level,source,message\nnot-a-date,INFO,app,Message\n")

    with pytest.raises(InvalidTimestampError) as exc_info:
        list(parse_csv(file))

    assert "line 2" in str(exc_info.value)


def test_cyrillic_content(tmp_path):
    """Тестирует обработку кириллических символов."""
    file = tmp_path / "cyrillic.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "2024-01-01T10:00:00,INFO,приложение,Запуск системы\n"
        "2024-01-01T11:00:00,ERROR,база данных,Ошибка подключения\n",
        encoding="utf-8",
    )

    events = list(parse_csv(file))

    assert len(events) == 2
    assert events[0].source == "приложение"
    assert events[0].message == "Запуск системы"
    assert events[1].source == "база данных"


def test_parse_csv_skip_invalid(tmp_path):
    """Тестирует пропуск невалидных строк в CSV."""
    file = tmp_path / "mixed.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "2024-01-01T10:00:00,INFO,app,OK\n"
        "BAD_DATE,INFO,app,Bad\n"
        "2024-01-01T12:00:00,ERROR,db,Fail\n"
    )

    events = list(parse_csv(file, skip_invalid=True))

    valid = [e for e in events if e is not None]
    skipped = [e for e in events if e is None]
    assert len(valid) == 2
    assert len(skipped) == 1


def test_get_parser_csv():
    """Тестирует получение парсера для CSV."""
    parser_func = get_parser("csv")
    assert parser_func is parse_csv


def test_get_parser_jsonl():
    """Тестирует получение парсера для JSONL."""
    parser_func = get_parser("jsonl")
    assert parser_func is parse_jsonl


def test_get_parser_unsupported():
    """Тестирует ошибку при неподдерживаемом формате."""
    with pytest.raises(UnsupportedFormatError):
        get_parser("xml")
