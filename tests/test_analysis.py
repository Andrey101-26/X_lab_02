from datetime import datetime

from streamstats.analysis import analyze_events
from streamstats.models import Event, Level


def test_analyze_events():
    """Тестирует подсчёт статистики."""
    events = [
        Event(datetime(2024, 1, 1, 10, 0), Level.INFO, "app", "Start"),
        Event(datetime(2024, 1, 1, 11, 0), Level.ERROR, "db", "Fail"),
        Event(datetime(2024, 1, 1, 12, 0), Level.ERROR, "db", "Fail again"),
        Event(datetime(2024, 1, 1, 13, 0), Level.INFO, "app", "End"),
    ]

    stats = analyze_events(iter(events))

    assert stats.total_events == 4
    assert stats.level_counts == {"INFO": 2, "ERROR": 2}
    assert stats.source_counts == {"app": 2, "db": 2}
    assert stats.error_source_counts == {"db": 2}
    assert stats.first_timestamp == datetime(2024, 1, 1, 10, 0)
    assert stats.last_timestamp == datetime(2024, 1, 1, 13, 0)
    assert stats.skipped_count == 0


def test_analyze_with_skipped():
    """Тестирует подсчёт с пропущенными строками."""
    events = [
        Event(datetime(2024, 1, 1, 10, 0), Level.INFO, "app", "OK"),
        None,
        Event(datetime(2024, 1, 1, 11, 0), Level.WARNING, "app", "Warn"),
    ]

    stats = analyze_events(iter(events))

    assert stats.total_events == 2
    assert stats.skipped_count == 1