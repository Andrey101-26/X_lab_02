# StreamStats

Потоковый анализатор лог-файлов в форматах CSV и JSONL.

## Возможности

- Потоковое чтение файлов (не загружает весь файл в память)
- Агрегация статистики без хранения всех событий
- Обработка ошибок с указанием номера строки
- Режим пропуска невалидных строк (--skip-invalid)
- Поддержка кириллицы и UTF-8
- Формирование JSON-отчёта с топ-5 источников ошибок
- Поддержка анализа нескольких файлов одновременно

## Установка

    pip install -e ".[dev]"

## Использование

### Анализ одного CSV-файла

    python -m streamstats analyze data.csv --format csv --output report.json

### Анализ JSONL-файла

    python -m streamstats analyze logs.jsonl --format jsonl --output report.json

### Анализ нескольких файлов

    python -m streamstats analyze file1.csv file2.csv --format csv --output report.json

### С пропуском невалидных строк

    python -m streamstats analyze data.csv --format csv --output report.json --skip-invalid

При использовании --skip-invalid невалидные строки пропускаются, а их количество записывается в поле skipped_count отчёта.

## Структура проекта

    lab_02/
    ├── src/
    │   └── streamstats/
    │       ├── __init__.py      # Инициализация пакета
    │       ├── __main__.py      # Точка входа CLI
    │       ├── analysis.py      # Агрегация статистики
    │       ├── errors.py        # Классы исключений
    │       ├── models.py        # Модели данных (Event, Level)
    │       ├── parsers.py       # Парсеры CSV и JSONL
    │       ── report.py        # Генерация отчёта
    ├── tests/
    │   ├── test_analysis.py     # Тесты анализа
    │   ├── test_cli.py          # Тесты CLI
    │   ├── test_parsers.py      # Тесты парсеров
    │   └── test_report.py       # Тесты отчёта
    ├── .gitignore
    ├── pyproject.toml           # Конфигурация проекта
    └── README.md

## Тестирование

    pytest                          
    ruff check                  

## Формат отчёта
    {
      "total_events": 100,
      "level_counts": {"INFO": 80, "ERROR": 15, "CRITICAL": 5},
      "source_counts": {"app": 60, "db": 40},
      "top_error_sources": [{"source": "db", "count": 20}],
      "first_timestamp": "2024-01-01T10:00:00",
      "last_timestamp": "2024-01-01T12:00:00",
      "skipped_count": 2
    }

Поля отчёта:

- total_events — общее количество обработанных событий
- level_counts — количество событий по уровням (INFO, WARNING, ERROR, CRITICAL)
- source_counts — количество событий по источникам
- top_error_sources — топ-5 источников с наибольшим количеством ошибок (ERROR и CRITICAL)
- first_timestamp — временная метка первого события
- last_timestamp — временная метка последнего события
- skipped_count — количество пропущенных невалидных строк

## Коды возврата

- 0 — успешное выполнение
- 2 — ошибка (невалидные аргументы, файл не найден, ошибка парсинга)