# StreamStats

Потоковый анализатор лог-файлов в форматах CSV и JSONL.


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