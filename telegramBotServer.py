import os
import telebot
import animeScrapper as animeAPI

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
print(TELEGRAM_API_KEY)
bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['get_all', 'help'])
def send_welcome(message):

	bot.send_message(message.chat.id, "Hello")

@bot.message_handler(commands=['get_manga', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Hello")

@bot.message_handler(commands=['get_anime', 'help'])
def send_welcome(message):
	returnMessage = "Anime update: \n"
	bot.send_message(message.chat.id, animeAPI.getAnimevostUpdates())


bot.polling()