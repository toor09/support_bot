from collections import namedtuple
from typing import List

Intent = namedtuple(
    "Intent",
    "display_name training_phrases text_messages"
)


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
