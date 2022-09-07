import logging
import logging.config

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

from settings import LOGGING_CONFIG, VKBotSettings

logger = logging.getLogger(__file__)
logging.config.dictConfig(LOGGING_CONFIG)


def start() -> None:
    """Start the vk bot."""
    settings = VKBotSettings()
    vk_session = vk_api.VkApi(token=settings.VK_GROUP_TOKEN)

    long_poll = VkLongPoll(vk_session)
    logger.debug(msg="Support VK Bot is started...")
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            logger.debug(msg="New message:")
            if event.to_me:
                logger.debug(msg=f"For me: {event.user_id}")
            else:
                logger.debug(msg=f"From me: {event.user_id}")
            logger.debug(msg=f"Message: {event.text}")


if __name__ == "__main__":
    start()
