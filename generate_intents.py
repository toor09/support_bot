import os

from dialog_flow import create_intent
from settings import DialogFlowSettings
from utils import download_training_phrases, get_intents, get_training_phrases


def main() -> None:
    """Create new intents at DialogFlow."""
    settings = DialogFlowSettings()
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        settings.GOOGLE_APPLICATION_CREDENTIALS  # type: ignore
    )
    download_training_phrases(
        url=(
            "https://dvmn.org/media/filer_public/a7/db/"
            "a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"
        ),
        filename="questions.json"
    )
    training_phrases = get_training_phrases()
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
