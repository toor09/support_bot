from typing import List, Optional

from google.cloud import dialogflow
from google.cloud.dialogflow import DetectIntentResponse


def detect_intent_texts(
        project_id: str,
        session_id: str,
        texts: List[str],
        language_code: str,
        skip_fallback: bool = False
) -> Optional[DetectIntentResponse]:
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.TextInput(
            text=text,
            language_code=language_code
        )
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    if skip_fallback and response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text


def create_intent(
        project_id: str,
        display_name: str,
        training_phrases_parts: List[str],
        message_texts: List[str]
) -> None:
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))
