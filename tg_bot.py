import logging
import logging.config

from telegram import ForceReply, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)

from settings import LOGGING_CONFIG, TelegramBotSettings

logger = logging.getLogger(__file__)
logging.config.dictConfig(LOGGING_CONFIG)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_creds = user.mention_markdown_v2()  # type: ignore
    update.message.reply_markdown_v2(
        fr"Hi {user_creds}\!",
        reply_markup=ForceReply(selective=True),
    )
    message = f"Support tg_bot send greeting message to: " \
              f"{user_creds}"
    logger.debug(msg=message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    message = "Support tg_bot send help message."
    logger.debug(msg=message)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    message = f"Support tg_bot send echo message:{update.message.text=}"
    logger.debug(msg=message)


def main() -> None:
    """Start the telegram bot."""
    settings = TelegramBotSettings()
    updater = Updater(settings.TG_BOT_TOKEN)
    logger.debug(msg="Support Telegram Bot is started...")

    dispatcher = updater.dispatcher  # type: ignore

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
