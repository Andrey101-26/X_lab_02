import csv
import json
from datetime import datetime

from .errors import InvalidEventError, InvalidTimestampError
from .models import Event, Level


def parse_csv(filepath, skip_invalid=False):
    """Читает CSV-файл построчно."""
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                yield _create_event(row, reader.line_num)
            except (InvalidEventError, InvalidTimestampError) as e:
                if skip_invalid:
                    print(f"Warning: Skipping line {reader.line_num}: {e}")
                    yield None
                else:
                    raise


def parse_jsonl(filepath, skip_invalid=False):
    """Читает JSONL-файл построчно."""
    with open(filepath, "r", encoding="utf-8") as file:
        for line_num, line in enumerate(file, start=1):
            if line.strip():
                try:
                    row = json.loads(line)
                    yield _create_event(row, line_num)
                except json.JSONDecodeError as e:
                    if skip_invalid:
                        print(f"Warning: Skipping line {line_num}: {e}")
                        yield None
                    else:
                        raise InvalidEventError(f"Invalid JSON at line {line_num}: {e}")
                except (InvalidEventError, InvalidTimestampError) as e:
                    if skip_invalid:
                        print(f"Warning: Skipping line {line_num}: {e}")
                        yield None
                    else:
                        raise


def _create_event(row, line_num):
    """Создаёт объект Event из строки."""
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

    return Event(timestamp, level, source, message)


def get_parser(format_name):
    """Возвращает парсер по имени формата."""
    if format_name == "csv":
        return parse_csv
    elif format_name == "jsonl":
        return parse_jsonl
    else:
        from .errors import UnsupportedFormatError
        raise UnsupportedFormatError(f"Unsupported format: {format_name}")