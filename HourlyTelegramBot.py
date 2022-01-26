import requests
from datetime import datetime, timedelta
import time
import pytz
import threading
import time
import os
import animeScrapper as animeAPI

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
tel_group_id = "EriksAnimeManagerBot"
time_interval = 10
S = set()


class loop:
    def wait(self, seconds):
        # This makes sure that when self.running is false it will instantly stop
        for a in range(seconds):
            if self.running:
                time.sleep(1)
            else:
                break

    def run(self, seconds):
        while self.running:
            # Runs function
            self.function()
            self.wait(seconds)

    def __init__(self, seconds, function):
        self.running = True
        self.function = function
        # Starts new thread instead of running it in the main thread
        # is because so it will not block other code
        self.thread = threading.Thread(target=self.run, args=(seconds,))
        self.thread.start()


def sendAnimeList():
    base_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=" {}"'.\
                format(TELEGRAM_API_KEY, tel_group_id, animeAPI.getAnimevostUpdates(S))
    print(base_url)
    requests.get(base_url)

a = loop(time_interval, sendAnimeList)