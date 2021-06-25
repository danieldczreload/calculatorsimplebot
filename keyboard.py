#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""
import logging

from simpleeval import simple_eval
from dotenv import load_dotenv, find_dotenv
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global vars
button_pressed = ""


def start(update: Update, context: CallbackContext) -> str:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            KeyboardButton("7"),
            KeyboardButton("8"),
            KeyboardButton("9"),
            KeyboardButton("*"),
        ],
        [
            KeyboardButton("4"),
            KeyboardButton("5"),
            KeyboardButton("6"),
            KeyboardButton("/"),
        ],
        [
            KeyboardButton("1"),
            KeyboardButton("2"),
            KeyboardButton("3"),
            KeyboardButton("-"),
        ],
        [
            KeyboardButton("0"),
            KeyboardButton("."),
            KeyboardButton("="),
            KeyboardButton("+"),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Input your operation:', reply_markup=reply_markup)
    return "custom_handler"


def calc(update: Update, context: CallbackContext):
    global button_pressed
    logging.info(update.message.text)
    logging.info(button_pressed)
    if update.message.text == "=":
        update.message.reply_text(simple_eval(button_pressed))
        button_pressed = ""
    else:
        button_pressed = button_pressed + update.message.text


def main() -> None:
    """Run the bot."""
    # loading env variables
    load_dotenv(find_dotenv())
    # Configuring login
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    TOKEN: str = os.getenv("TOKEN")
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command),
                       calc))  # resend confirmation email

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
