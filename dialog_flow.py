from typing import List

from google.cloud import dialogflow
from google.cloud.dialogflow import DetectIntentResponse


def detect_intent_texts(
        project_id: str,
        session_id: str,
        texts: List[str],
        language_code: str
) -> DetectIntentResponse:
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

    return response.query_result.fulfillment_text
