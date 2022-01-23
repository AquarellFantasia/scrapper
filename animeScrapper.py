from bs4 import BeautifulSoup
import requests

def getAnimevostUpdates():
    # List of titles to get update on
    list_of_titles = ["Герой-рационал перестраивает королевство",
                      "фарфоровая",
                      "Магическая битва",
                      "Рейтинг короля",
                      "Арифурэта"]
    returnString = ""

    #get html page
    url = "https://animevost.org/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # get all divs with names as a list
    names = doc.find_all('div', {"class": "shortstoryHead"})
    # Form a string
    for arg in names:
        if any(title in arg.find('a').string for title in list_of_titles):
            returnString += "-"
            returnString += arg.find('a').string
            returnString += "\n"
    return returnString

