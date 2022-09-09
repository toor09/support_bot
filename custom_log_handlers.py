import logging

import telegram


class TelegramLogsHandler(logging.Handler):
    """Custom telegram handler for logging."""
    def __init__(self, token: str, chat_id: str) -> None:
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord) -> None:
        tg_bot = telegram.Bot(token=self.token)
        tg_bot.send_message(chat_id=self.chat_id, text=self.format(record))
