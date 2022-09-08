import json
import logging
from collections import namedtuple
from typing import List

import requests
import telegram

Intent = namedtuple(
    "Intent",
    "display_name training_phrases text_messages"
)


class TelegramLogsHandler(logging.Handler):
    """Custom telegram handler for logging."""
    def __init__(self, token: str, chat_id: str) -> None:
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord) -> None:
        tg_bot = telegram.Bot(token=self.token)
        tg_bot.send_message(chat_id=self.chat_id, text=self.format(record))


def get_training_phrases(filename: str = "questions.json") -> dict:
    """Get training_phrases from json file."""
    with open(filename, "r") as file:
        training_phrases = json.load(file)
    return training_phrases


def get_intents(training_phrases: dict) -> List[Intent]:
    """Get collection of new intents."""
    intents = []
    for training_phrase in training_phrases:
        display_name = training_phrase
        new_intent = Intent(
            display_name=training_phrase,
            training_phrases=training_phrases[display_name]["questions"],
            text_messages=[training_phrases[display_name]["answer"]],
        )
        intents.append(new_intent)

    return intents


def download_training_phrases(
        url: str,
        filename: str
) -> None:
    """Download training phrases from remote storage."""
    training_phrases = requests.get(url=url)
    training_phrases.raise_for_status()

    with open(file=filename, mode="wb") as file:
        file.write(training_phrases.content)
