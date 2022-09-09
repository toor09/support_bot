import json
import os
from typing import Optional

import click
import requests
from pathvalidate import sanitize_filepath

from dialog_flow import create_intent
from intents_operations import get_intents
from settings import DialogFlowSettings


@click.command()
@click.option(
    "-J", "--json-path",
    default=None,
    help="Path for loading training phrases from local file."
)
def main(json_path: Optional[str]) -> None:
    """Create new intents at DialogFlow."""
    settings = DialogFlowSettings()
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        settings.GOOGLE_APPLICATION_CREDENTIALS  # type: ignore
    )
    default_filename = "questions.json"

    if settings.STORAGE_FILE_URL:
        questions = requests.get(url=settings.STORAGE_FILE_URL)
        questions.raise_for_status()
        with open(file=default_filename, mode="wb") as file:
            file.write(questions.content)

    filename = f"{sanitize_filepath(json_path, platform='auto')}" \
        if json_path else default_filename

    with open(file=filename, mode="r") as file:
        training_phrases = json.load(file)

    intents = get_intents(training_phrases)
    for intent in intents:
        create_intent(
            project_id=settings.PROJECT_ID,
            display_name=intent.display_name,
            training_phrases_parts=intent.training_phrases,
            message_texts=intent.text_messages
        )


if __name__ == "__main__":
    main()
