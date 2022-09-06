import logging
import logging.config
import os

import telegram.error
from google.auth.exceptions import DefaultCredentialsError
from telegram import ForceReply, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)

from dialog_flow import detect_intent_texts
from settings import LOGGING_CONFIG, DialogFlowSettings, TelegramBotSettings

logger = logging.getLogger(__file__)
logging.config.dictConfig(LOGGING_CONFIG)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_creds = user.mention_markdown_v2()  # type: ignore
    update.message.reply_markdown_v2(
        fr"Привет {user_creds}\!",
        reply_markup=ForceReply(selective=True),
    )
    message = f"Support tg_bot send greeting message to: " \
              f"{user_creds=}"
    logger.debug(msg=message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    message = "Support tg_bot send help message."
    logger.debug(msg=message)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    settings = DialogFlowSettings()
    user = update.effective_user
    try:
        dialog_flow_answer = detect_intent_texts(
                project_id=settings.PROJECT_ID,
                session_id=user.id,  # type: ignore
                texts=[update.message.text],
                language_code="ru",
        )
        update.message.reply_text(f"{dialog_flow_answer}")
        message = f"Support tg_bot send echo message:" \
                  f"{update.message.text=} {dialog_flow_answer=}"
        logger.debug(msg=message)

    except DefaultCredentialsError:
        message = "Something is wrong with connecting to DialogFlow :("
        logger.error(msg=message, exc_info=True)

    except telegram.error.NetworkError:
        message = "Something went wrong :("
        logger.error(msg=message, exc_info=True)


def main() -> None:
    """Start the telegram bot."""
    tg_settings = TelegramBotSettings()
    df_settings = DialogFlowSettings()
    updater = Updater(tg_settings.TG_BOT_TOKEN)
    logger.debug(msg="Support Telegram Bot is started...")
    os.environ.setdefault(
        "GOOGLE_APPLICATION_CREDENTIALS",
        df_settings.GOOGLE_APPLICATION_CREDENTIALS  # type: ignore
    )

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
