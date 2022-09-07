import sys
from pathlib import Path

from pathvalidate import sanitize_filepath
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


class DialogFlowSettings(Settings):
    GOOGLE_APPLICATION_CREDENTIALS: Path
    PROJECT_ID: str

    @validator("GOOGLE_APPLICATION_CREDENTIALS")
    def google_application_credentials(cls, v: Path) -> str:
        if v == Path('.'):
            raise ValueError(
                "The value of GOOGLE_APPLICATION_CREDENTIALS is not set."
            )
        return f"{sanitize_filepath(file_path=v, platform='auto')}"


class TelegramBotSettings(Settings):
    TG_BOT_TOKEN: str


class VKBotSettings(Settings):
    VK_GROUP_TOKEN: str


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
        "rotating_vk_bot_to_file": {
            "level": Settings().LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "support_vk_bot.log",
            "maxBytes": 10000,
            "backupCount": 10,
        },
    },
    "loggers": {
        "tg_bot": {
            "handlers": ["default", "rotating_tg_bot_to_file"],
            "level": Settings().LOGGING_LEVEL,
            "propagate": True
        },
        "vk_bot": {
            "handlers": ["default", "rotating_vk_bot_to_file"],
            "level": Settings().LOGGING_LEVEL,
            "propagate": True
        }
    }
}
