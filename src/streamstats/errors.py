class StreamStatsError(Exception):
    """Базовый класс для всех исключений пакета streamstats."""


class UnsupportedFormatError(StreamStatsError):
    """Вызывается при передаче неподдерживаемого формата файла."""


class InvalidEventError(StreamStatsError):
    """Вызывается при невалидных данных события."""


class InvalidTimestampError(StreamStatsError):
    """Вызывается при невалидном формате временной метки."""


class CLIConfigError(StreamStatsError):
    """Вызывается при ошибке в аргументах командной строки."""
