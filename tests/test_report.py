import json
from datetime import datetime

from streamstats.analysis import Stats
from streamstats.report import generate_report


def test_generate_report(tmp_path):
    """Тестирует формирование JSON-отчёта."""
    stats = Stats(
        total_events=3,
        level_counts={"INFO": 1, "ERROR": 1, "CRITICAL": 1},
        source_counts={"app": 1, "db": 2},
        error_source_counts={"db": 2},
        first_timestamp=datetime(2024, 1, 1, 10, 0),
        last_timestamp=datetime(2024, 1, 1, 12, 0),
        skipped_count=1,
    )

    output_file = tmp_path / "report.json"
    generate_report(stats, output_file)

    with open(output_file) as f:
        report = json.load(f)

    assert report["total_events"] == 3
    assert report["skipped_count"] == 1
    assert len(report["top_error_sources"]) == 1
    assert report["top_error_sources"][0]["source"] == "db"


def test_top_error_sources_limit(tmp_path):
    """Тестирует, что top_error_sources содержит не более 5 источников."""
    error_sources = {f"src_{i}": 10 - i for i in range(10)}
    stats = Stats(error_source_counts=error_sources)

    output_file = tmp_path / "report.json"
    generate_report(stats, output_file)

    with open(output_file) as f:
        report = json.load(f)

    assert len(report["top_error_sources"]) == 5
