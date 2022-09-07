import logging
import logging.config
from random import randint
from typing import Any

from vk_api import VkApi
from vk_api.longpoll import Event, VkEventType, VkLongPoll

from settings import LOGGING_CONFIG, VKBotSettings

logger = logging.getLogger(__file__)
logging.config.dictConfig(LOGGING_CONFIG)


def echo(event: Event, vk_api: Any) -> None:
    """Echo the user message."""
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=randint(1, 1000)
    )
    logger.debug(msg=f"User: {event.user_id}")
    logger.debug(msg=f"Echo Message: {event.text}")


def start() -> None:
    """Start the vk bot."""
    settings = VKBotSettings()
    vk_session = VkApi(token=settings.VK_GROUP_TOKEN)
    vk_api = vk_session.get_api()
    long_poll = VkLongPoll(vk_session)

    logger.debug(msg="Support VK Bot is started...")
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == "__main__":
    start()
