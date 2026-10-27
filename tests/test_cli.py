import json
import subprocess


def test_cli_help():
    """Тестирует вывод справки CLI."""
    result = subprocess.run(
        ["python", "-m", "streamstats", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "analyze" in result.stdout


def test_cli_analyze_csv(tmp_path):
    """Тестирует анализ CSV через CLI."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "timestamp,level,source,message\n2024-01-01T10:00:00,INFO,app,Start\n"
    )

    output_file = tmp_path / "report.json"

    result = subprocess.run(
        [
            "python",
            "-m",
            "streamstats",
            "analyze",
            str(csv_file),
            "--format",
            "csv",
            "--output",
            str(output_file),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()


def test_cli_multiple_files(tmp_path):
    """Тестирует анализ нескольких файлов сразу."""
    file1 = tmp_path / "file1.csv"
    file1.write_text(
        "timestamp,level,source,message\n2024-01-01T10:00:00,INFO,app,Start\n"
    )

    file2 = tmp_path / "file2.csv"
    file2.write_text(
        "timestamp,level,source,message\n2024-01-01T11:00:00,ERROR,db,Fail\n"
    )

    output_file = tmp_path / "report.json"

    result = subprocess.run(
        [
            "python",
            "-m",
            "streamstats",
            "analyze",
            str(file1),
            str(file2),
            "--format",
            "csv",
            "--output",
            str(output_file),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    with open(output_file) as f:
        report = json.load(f)

    assert report["total_events"] == 2


def test_cli_exit_code_on_error(tmp_path):
    """Тестирует код выхода 2 при ошибке."""
    result = subprocess.run(
        [
            "python",
            "-m",
            "streamstats",
            "analyze",
            "nonexistent.csv",
            "--format",
            "csv",
            "--output",
            str(tmp_path / "report.json"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
