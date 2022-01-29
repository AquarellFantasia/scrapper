import telepot
import os
from pprint import pprint




TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = telepot.Bot(TELEGRAM_API_KEY)
bot.sendMessage(999999999, 'Hey!')
