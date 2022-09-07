import logging
import logging.config
import os
from random import randint
from typing import Any

from google.auth.exceptions import DefaultCredentialsError
from vk_api import VkApi
from vk_api.longpoll import Event, VkEventType, VkLongPoll

from dialog_flow import detect_intent_texts
from settings import LOGGING_CONFIG, DialogFlowSettings, VKBotSettings

logger = logging.getLogger(__file__)
logging.config.dictConfig(LOGGING_CONFIG)


def echo(event: Event, vk_api: Any, project_id: str) -> None:
    """Echo the user message."""
    try:
        dialog_flow_answer = detect_intent_texts(
                project_id=project_id,
                session_id=event.user_id,
                texts=[event.text],
                language_code="ru",
        )
        vk_api.messages.send(
            user_id=event.user_id,
            message=f"{dialog_flow_answer}",
            random_id=randint(1, 1000)
        )
        message = f"Support tg_bot send echo message:" \
                  f"{event.text=} {dialog_flow_answer=}"
        logger.debug(msg=message)

    except DefaultCredentialsError:
        message = "Something is wrong with connecting to DialogFlow :("
        logger.error(msg=message, exc_info=True)


def start() -> None:
    """Start the vk bot."""
    settings = VKBotSettings()
    df_settings = DialogFlowSettings()

    vk_session = VkApi(token=settings.VK_GROUP_TOKEN)
    vk_api = vk_session.get_api()

    long_poll = VkLongPoll(vk_session)
    logger.debug(msg="Support VK Bot is started...")
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        df_settings.GOOGLE_APPLICATION_CREDENTIALS  # type: ignore
    )
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(
                event=event,
                vk_api=vk_api,
                project_id=df_settings.PROJECT_ID
            )


if __name__ == "__main__":
    start()
