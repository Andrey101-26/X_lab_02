import json
from pathlib import Path

from .analysis import Stats


def generate_report(stats: Stats, output_path: Path) -> None:
    """Формирует JSON-отчёт из статистики."""
    top_errors = sorted(stats.error_source_counts.items(), key=lambda x: (-x[1], x[0]))[
        :5
    ]

    report = {
        "total_events": stats.total_events,
        "level_counts": stats.level_counts,
        "source_counts": stats.source_counts,
        "top_error_sources": [
            {"source": source, "count": count} for source, count in top_errors
        ],
        "first_timestamp": stats.first_timestamp.isoformat()
        if stats.first_timestamp
        else None,
        "last_timestamp": stats.last_timestamp.isoformat()
        if stats.last_timestamp
        else None,
        "skipped_count": stats.skipped_count,
    }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
