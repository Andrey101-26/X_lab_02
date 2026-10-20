import subprocess


def test_cli_help():
    """Тестирует вывод справки CLI."""
    result = subprocess.run(
        ["python", "-m", "streamstats", "--help"],
        check=False,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "analyze" in result.stdout


def test_cli_analyze_csv(tmp_path):
    """Тестирует анализ CSV через CLI."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("timestamp,level,source,message\n2024-01-01T10:00:00,INFO,app,Start\n")

    output_file = tmp_path / "report.json"

    result = subprocess.run(
        [
            "python", "-m", "streamstats", "analyze",
            str(csv_file), "--format", "csv", "--output", str(output_file)
        ],
        check=False,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert output_file.exists()