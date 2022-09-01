import sys

from pydantic import BaseSettings, validator

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    LOGGING_LEVEL: str = "WARNING"

    @validator("LOGGING_LEVEL")
    def logging_levels(cls, v: str) -> str:
        if v.upper() not in LEVELS:
            raise ValueError(
                f"The value is not in the list of required: {LEVELS}"
            )
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"


class TelegramBotSettings(Settings):
    TG_BOT_TOKEN: str


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": Settings().LOGGING_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
        },
        "rotating_tg_bot_to_file": {
            "level": Settings().LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "support_tg_bot.log",
            "maxBytes": 10000,
            "backupCount": 10,
        },
    },
    "loggers": {
        "tg_bot": {
            "handlers": ["default", "rotating_tg_bot_to_file"],
            "level": Settings().LOGGING_LEVEL,
            "propagate": True
        }
    }
}
