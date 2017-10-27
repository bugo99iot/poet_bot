import os
import telebot

#token encripted as: $ export BOT_API_TOKEN="<paste the token here>"
#token = os.environ['BOT_API_TOKEN']

token = "460636751:AAHxhE3ftINDzYKGw4OvuMHRVUy_cCEsbxw"

bot = telebot.TeleBot(token)

#send message when command is entered, such as /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, u"Hello, you asked for help or start!")

#Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
	bot.reply_to(message, u"I bet you wrote something!")

#echo input from user
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)


bot.polling()
