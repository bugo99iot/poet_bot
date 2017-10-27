# -*- coding: utf-8 -*-

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler
import requests
import json
import datetime
import time

token = "460636751:AAHxhE3ftINDzYKGw4OvuMHRVUy_cCEsbxw"
admin = ["pseudo1", "pseudo2"]

def start(bot, update):
    print update.message.chat.username
    t = """Hello %s, you can check the current train schedule of SBB-CFF with my help,
    type /help to see the commands, Bon Voyage!""" % update.message.chat.first_name
    bot.sendMessage(chat_id=update.message.chat_id, text=t)


def help(bot, update):
    t = """Use /iliketrains or /trains <Departure> <Destination> <Time(HH:MM)> to get next immediate connections
    from your location, note that 'Time' is optional"""
    bot.sendMessage(chat_id=update.message.chat_id, text=t)


def stop(bot, update):
    if update.message.chat.username in admin:
        updater.stop_polling()
        updater.stop()


def trains(bot, update, args):
    # print args

    for i in range(0, len(args)):

        if len(args) == 2:
            info = stations(args[0], args[1])
        elif len(args) == 3:
            info = stations(args[0], args[1], args[2])

    bot.sendMessage(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)


def hms_to_minutes(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 60*h + m


def stations(dep_loc, arr_loc, time = ""):
    url_str = "http://transport.opendata.ch/v1/connections?from=%s&to=%s"

    if time == '':
        url_str = url_str % (dep_loc, arr_loc)
    else:
        url_str = "http://transport.opendata.ch/v1/connections?from=%s&to=%s&time=%s" % (dep_loc, arr_loc, time)

    response = requests.get(url_str)

    r = response.content

    r = json.loads(r)
    i = 0
    res = "Connections from *" + r['connections'][i]['from']['location']['name'] + "* to *" + r['to']['name'] + "* \n\n"

    nontrains = ["BUS", "M", "NFB"]

    for i in range(0, len(r['connections'])):

        for j in range(0, len(r['connections'][i]['sections'])):

            if not r['connections'][i]['sections'][j]['walk']:

                timestamp = r['connections'][i]['sections'][j]['departure']['departureTimestamp']
                timeDep = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')

                timestamp = r['connections'][i]['sections'][j]['arrival']['arrivalTimestamp']
                timeArr = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')

                if r['connections'][i]['sections'][j]['journey']['category'] in nontrains:
                    res += " \[" + r['connections'][i]['sections'][j]['journey']['category'] + "] "
                    res += r['connections'][i]['sections'][j]['departure']['station']['name'] + " \[*" + timeDep + "*] "
                    res += " --> " + r['connections'][i]['sections'][j]['arrival']['station']['name'] + " \[*" + timeArr + "*] \n"
                else:
                    res += " \[" + r['connections'][i]['sections'][j]['journey']['category'] + "] "
                    res += r['connections'][i]['sections'][j]['departure']['station']['name'] + " \[*" + timeDep + "*] (P" + r['connections'][i]['sections'][j]['departure']['platform'] + ")"
                    res += " --> " + r['connections'][i]['sections'][j]['arrival']['station']['name'] + " \[*" + timeArr + "*] (P" + r['connections'][i]['sections'][j]['arrival']['platform']  + ") \n"

            else:
                t = r['connections'][i]['sections'][j]['walk']['duration']
                res += " \[Walk] "
                res += "%d minutes \n" % hms_to_minutes(t)

        res += "\n"

    return res


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(token=token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('iliketrains', trains, pass_args=True))
    dp.add_handler(CommandHandler('trains', trains, pass_args=True))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('help', help))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
