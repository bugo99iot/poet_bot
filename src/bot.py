from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import telegram

from src.poet import Poet
import nltk
import os
nltk.download('punkt')
nltk.download('stopwords')

load_dotenv(find_dotenv("env"))

directory_path = os.path.dirname(os.path.realpath(__file__))

df_tokenized = pd.read_csv(directory_path + "/scraper_ML/tokenized_poems.csv")
df_poems = pd.read_csv(directory_path + "/scraper_ML/poems_collection.csv")

import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

WANT_POEM_YES_NO, WANT_POEM_TOPIC = range(2)

reply_keyboard = [['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start_conversation(bot, update):

    user_input = update.message.text

    logging.warning(update.message.chat.first_name)
    logging.warning(update.message.text)

    t = ("Hello {}, this is PoetBot. Would you like to read a poem?".format(update.message.chat.first_name))

    update.message.reply_text(text=t)

    return WANT_POEM_YES_NO


def want_poem_yes_no(bot, update):
    text = update.message.text
    if "yes" in text:
        update.message.reply_text("Great! Topic?")
        return WANT_POEM_TOPIC
    else:
        update.message.reply_text("Bummer!")
        time.sleep(5)
        return start_conversation(bot, update)


def want_poem_topic(bot, update):

    text = update.message.text
    target_poem = Poet(text, df_poems=df_poems, df_tokenized=df_tokenized).get_poem

    if target_poem is None:
        update.message.reply_text("Sorry, could not find your poem. Try again.")
        time.sleep(5)
        return start_conversation(bot, update)

    title, body, author = target_poem.get("title"), target_poem.get("body"), target_poem.get("author")

    t = "*" + title.replace("<br/>", "\n") + "*" + "\n" + "\n" + body.replace("<br/>",
                                                                              "\n").strip() + "\n" + "\n" + "_" + "by " + author.replace(
        "<br/>", "\n") + "_"

    bot.sendMessage(chat_id=update.message.chat_id, text=t,
                    parse_mode=telegram.ParseMode.MARKDOWN)

    #update.message.reply_text(text=t)

    time.sleep(2)
    restart = "Wanna play again? Type /start to start again or just search for the next poem."
    return start_conversation(bot, update)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token="739863186:AAGgESP4fYSAHs0uNV9isXdoibl3NRAgoMI")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start_conversation)],

        states={

            WANT_POEM_YES_NO: [MessageHandler(Filters.text,
                                          want_poem_yes_no)],
            WANT_POEM_TOPIC: [MessageHandler(Filters.text,
                                              want_poem_topic)],
        },

        fallbacks=[RegexHandler(Filters.text, start_conversation)]
    )

    #dp.add_handler(MessageHandler(Filters.text, start_conversation))

    dp.add_handler(conv_handler)

    # dp.add_handler(MessageHandler(Filters.text, converse))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

