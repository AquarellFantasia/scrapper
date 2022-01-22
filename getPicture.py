from bs4 import BeautifulSoup
import requests

list_of_titles = ["Герой-рационал перестраивает королевство", "фарфоровая"]

#get documents
url = "https://animevost.org/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")



names = doc.find_all('div', {"class": "shortstoryHead"})
for arg in names:
    if any(title in arg.find('a').string for title in list_of_titles):
        print(arg.find('a').string)


