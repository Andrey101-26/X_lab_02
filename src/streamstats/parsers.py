import csv
import json
import logging
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from .errors import InvalidEventError, InvalidTimestampError
from .models import Event, Level

logger = logging.getLogger(__name__)


def parse_csv(filepath: Path, skip_invalid: bool = False) -> Iterator[Event | None]:
    """Читает CSV-файл построчно и возвращает события через генератор."""
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                yield _validate_and_create_event(row, reader.line_num)
            except (InvalidEventError, InvalidTimestampError) as e:
                if skip_invalid:
                    logger.warning(f"Skipping invalid line {reader.line_num}: {e}")
                    yield None
                else:
                    raise


def parse_jsonl(filepath: Path, skip_invalid: bool = False) -> Iterator[Event | None]:
    """Читает JSONL-файл построчно и возвращает события через генератор."""
    with open(filepath, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            if line.strip():
                try:
                    row = json.loads(line)
                    yield _validate_and_create_event(row, line_num)
                except json.JSONDecodeError as e:
                    if skip_invalid:
                        logger.warning(f"Skipping invalid JSON at line {line_num}: {e}")
                        yield None
                    else:
                        raise InvalidEventError(f"Invalid JSON at line {line_num}: {e}")
                except (InvalidEventError, InvalidTimestampError) as e:
                    if skip_invalid:
                        logger.warning(f"Skipping invalid line {line_num}: {e}")
                        yield None
                    else:
                        raise


def _validate_and_create_event(row: dict, line_num: int) -> Event:
    """Проверяет поля строки и создаёт объект Event."""
    timestamp_str = row.get("timestamp", "")
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
    except ValueError as e:
        raise InvalidTimestampError(f"Invalid timestamp at line {line_num}: {e}")

    level_str = row.get("level", "")
    try:
        level = Level(level_str)
    except ValueError as e:
        raise InvalidEventError(f"Invalid level at line {line_num}: {e}")

    source = row.get("source", "")
    message = row.get("message", "")

    if not source:
        raise InvalidEventError(f"Source is empty at line {line_num}")

    return Event(
        timestamp=timestamp,
        level=level,
        source=source,
        message=message
    )


def get_parser(format_name: str):
    """Возвращает парсер по имени формата."""
    parsers = {
        "csv": parse_csv,
        "jsonl": parse_jsonl,
    }
    if format_name not in parsers:
        from .errors import UnsupportedFormatError
        raise UnsupportedFormatError(f"Unsupported format: {format_name}")
    return parsers[format_name]