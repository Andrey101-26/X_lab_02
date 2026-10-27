import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime

from .models import Event, Level

logger = logging.getLogger(__name__)


@dataclass
class Stats:
    """Хранит агрегированную статистику по событиям."""

    total_events: int = 0
    level_counts: dict[str, int] = field(default_factory=dict)
    source_counts: dict[str, int] = field(default_factory=dict)
    error_source_counts: dict[str, int] = field(default_factory=dict)
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None
    skipped_count: int = 0


def analyze_events(events: Iterator[Event | None]) -> Stats:
    """Обрабатывает поток событий и собирает статистику."""
    stats = Stats()

    for item in events:
        if item is None:
            stats.skipped_count += 1
            continue

        event = item
        stats.total_events += 1

        level_name = event.level.value
        stats.level_counts[level_name] = stats.level_counts.get(level_name, 0) + 1

        stats.source_counts[event.source] = stats.source_counts.get(event.source, 0) + 1

        if event.level in (Level.ERROR, Level.CRITICAL):
            stats.error_source_counts[event.source] = (
                stats.error_source_counts.get(event.source, 0) + 1
            )

        if stats.first_timestamp is None or event.timestamp < stats.first_timestamp:
            stats.first_timestamp = event.timestamp

        if stats.last_timestamp is None or event.timestamp > stats.last_timestamp:
            stats.last_timestamp = event.timestamp

    return stats
