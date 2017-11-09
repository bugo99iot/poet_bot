#import stuff
#note, to run this you mst use python3

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import datetime
import time
import pandas as pd
import logging
from poet_class import Poet

#import logger, this gives you info on terminal about what happens to the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

#insert here the token delivered to you by BotFather
token = "464737464hfgrjrgrf65734636djusdh746464JFHDHDEYD"

#this is the command you may tyoe in to restart PoetBot (pretty useless)
def start(bot, update):
    print(update.message.chat.username)
    t = ("Hello %s, this is PoetBot. What kind of poem would you like to read?" + "\n" + "Type /poem followed by a list of key-words. If you struggle, type /help.") % update.message.chat.first_name
    bot.sendMessage(chat_id=update.message.chat_id, text=t)

#whatever you type into poet bot, he will echo the start message again and again (unless you use a command)
def echo(bot, update):
    #t = update.message.text + " eccome"
    print(update.message.chat.username)
    t = ("Hello %s, this is PoetBot. What kind of poem would you like to read?" + "\n" + "Type /poem followed by a list of key-words. If you struggle, type /help.") % update.message.chat.first_name
    bot.send_message(chat_id=update.message.chat_id, text=t)

#this defines the /help command
def help(bot, update):
    t = "Would you like to read a poem about THE UNIVERSE!! " + "\n" + "Type: /poem universe"
    bot.sendMessage(chat_id=update.message.chat_id, text=t)

#we upload the database containing all poems from which to choose
df_poems = pd.read_csv("poems_collection.csv", header=None)

#we define a command to print a poem to Telegram
#the command is used as follow: typing '/poem dinosaur' to the bot will print a poem about dinosaurs 
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
    restart = "Wanna play again? Type /start to start again or just search for the next poem."
    bot.sendMessage(chat_id=update.message.chat_id, text=restart,parse_mode=telegram.ParseMode.MARKDOWN)

#defining a function printing errors
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

#activate all commands and functions
def main():
    updater = Updater(token=token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    #this one is for the echo function, slightly different from the others
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler('poem', poem, pass_args=True))
    dp.add_handler(CommandHandler('help', help))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
