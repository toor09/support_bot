import json
from collections import namedtuple
from typing import List

import requests

Intent = namedtuple(
    "Intent",
    "display_name training_phrases text_messages"
)


def download_training_phrases(
        url: str,
        filename: str
) -> None:
    """Download training phrases from remote storage."""
    training_phrases = requests.get(url=url)
    training_phrases.raise_for_status()

    with open(file=filename, mode="wb") as file:
        file.write(training_phrases.content)


def get_training_phrases(filename: str = "questions.json") -> dict:
    """Get training_phrases from json file."""
    with open(filename, "r") as file:
        training_phrases = json.load(file)
    return training_phrases


def get_intents(training_phrases: dict) -> List[Intent]:
    """Get collection of new intents."""
    intents = []
    for display_name, training_phrase in training_phrases.items():
        new_intent = Intent(
            display_name=display_name,
            training_phrases=training_phrase["questions"],
            text_messages=[training_phrase["answer"]],
        )
        intents.append(new_intent)
    return intents
