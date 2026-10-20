from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Level(str, Enum):
    """Перечисление допустимых уровней событий."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class Event:
    """Модель события с обязательными полями."""
    timestamp: datetime
    level: Level
    source: str
    message: str