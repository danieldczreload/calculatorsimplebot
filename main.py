from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext
from dotenv import load_dotenv, find_dotenv
from simpleeval import simple_eval
from uuid import uuid4
import logging
import os


def start(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I am a calculator, please give me some "
                                                                    "operations to solve")


def calculate(update: Update, context: CallbackContext) -> int:
    operation = ''.join(context.args).upper()
    result = simple_eval(operation)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    update.message.reply_text(result)


def meme(update: Update, context: CallbackContext) -> int:
    context.bot.send_photo(update.effective_chat.id,
                           "https://statics.memondo.com/p/99/ccs/2011/01"
                           "/CC_26174_d73475cb3b8e4d45888cedbb1ffc7a58_trollface_verdad_incomoda.jpg?cb=8297780")


def inline_calculate(update: Update, context: CallbackContext) -> int:
    query = update.inline_query.query
    if not query:
        return 0
    results = list()
    logging.info(str(uuid4()))
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=query,
            input_message_content=InputTextMessageContent(simple_eval(query))
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main() -> None:
    """Run the calculator bot"""
    # loading env variables
    load_dotenv(find_dotenv())
    # Configuring login
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    TOKEN: str = os.getenv("TOKEN")
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # calc command
    calculate_handler = CommandHandler('calc', calculate)
    dispatcher.add_handler(calculate_handler)

    # meme command
    meme_handler = CommandHandler('meme', meme)
    dispatcher.add_handler(meme_handler)

    # inline query command
    inline_calculate_handler = InlineQueryHandler(inline_calculate)
    dispatcher.add_handler(inline_calculate_handler)

    # Unknown command
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
