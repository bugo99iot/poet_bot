# -*- coding: utf-8 -*-
#useful telegram tutorial: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets
#useful code example: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/inlinebot.py

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler
import requests
import json
import datetime
import time
import pandas as pd
import logging
from poet_class import Poet



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

token = "yourtoken"

def start(bot, update):
    print(update.message.chat.username)
    t = ("Hello %s, this is PoetBot. What kind of poem would you like to read?" + "\n" + "Type /poem followed by a list of key-words. If you struggle, type /help.") % update.message.chat.first_name
    bot.sendMessage(chat_id=update.message.chat_id, text=t)

def echo(bot, update, args):
    t = update.message.text + "eccome" + args
    bot.send_message(chat_id=update.message.chat_id, text=t)

def help(bot, update):
    t = "Would you like to read a poem about THE UNIVERSE!! " + "\n" + "Type: /poem universe"
    bot.sendMessage(chat_id=update.message.chat_id, text=t)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    print(text_caps)
    print(args)
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


df_poems = pd.read_csv("poems_collection.csv", header=None)

def poem(bot,update, args):
    #args = str(' '.join(args))
    #print(type(args))
    print("user %s %s just requested a poem" % (update.message.chat.first_name,update.message.chat.last_name))
    user_input = " ".join(args).strip()
    #create instance of poet class
    poet_object = Poet(user_input)
    #get target poem
    target_poem = poet_object.get_poem()

    t = "*" + target_poem[1].replace("<br/>","\n") + "*" + "\n" + "\n" + target_poem[0].replace("<br/>","\n").strip() + "\n" + "\n" + "_" + "by " + target_poem[2].replace("<br/>","\n") + "_"
    bot.sendMessage(chat_id=update.message.chat_id, text=t,parse_mode=telegram.ParseMode.MARKDOWN)
    restart = "Wanna play again? Type /start to start again."
    bot.sendMessage(chat_id=update.message.chat_id, text=restart,parse_mode=telegram.ParseMode.MARKDOWN)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(token=token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('echo', echo)) 
    dp.add_handler(CommandHandler('caps', caps, pass_args=True))
    dp.add_handler(CommandHandler('poem', poem, pass_args=True))
    dp.add_handler(CommandHandler('help', help))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
