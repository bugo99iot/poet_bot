# poet_bot

Building a Telegram chatbot which recommends poems based on input strings.

# Data

I have scraped the 500 most popular poems from a dedicated website (see 'poems_scrape.ipynb'). The results are in 'poems_collection.csv', with columns labelled as author, title, text. Text contains <br\/> elements to improve aestherics when printed out (<br\/> -> \n).

# Bot usage

In case you would like to chat with PoetBot:
1) Download the Telegram app to your phone and create an account. 2) Search for 'VioletsAreBlueBot'. 3) Chat with the bot :) 4) Note that I run the bot locally, hence it will reply only if my server is running.

In case you would like to run the bot on your machine:
1) Download the Telegram app to your phone and create an account. 2) Connect to BotFather. 3) Create a bot with given name and username. 4) Save your token. 5) Download the code from this repo to your local machine. 6) Replace your token in 'bot.py' 7) Run 'python3 bot.py'. 8) Find your new bot on Telegram using 'username' 9) Have a chat :) 

# Result

Have a look at [this snapshot] to see what PoetBot looks like.

# Blog

I have written about this project on [Medium].

# License
Released under version 2.0 of the [Apache License].

[Apache license]: http://www.apache.org/licenses/LICENSE-2.0
[this snapshot]: https://github.com/bugo99iot/poet_bot/blob/master/snapbot1.jpg
[Medium]: https://medium.com/@ugo.bertello/poetbot-2-a-telegram-chat-bot-for-poem-recommendation-70d1b809761c
