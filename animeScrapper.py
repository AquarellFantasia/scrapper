from bs4 import BeautifulSoup
import requests


def getAnimevostUpdates(s):
    # List of titles to get update on
    list_of_titles = ["Герой-рационал",
                      "фарфоровая кукла",
                      "Магическая битва",
                      "Рейтинг короля",
                      "Арифурэта",
                      "Повелитель",
                      "Реинкарнация безработного",
                      "Ванпанчмен",
                      "Блич",
                      "Восхождение героя щита"
                      "Haikyuu",
                      "О моём перерождении в слизь",
                      "Мастера меча онлайн",
                      "Жизнь в альтернативном мире с нуля",
                      "Убийца гоблинов",
                      "Вторжение Гигантов",
                      "Повесть о конце света",
                      "Доктор Стоун",
                      "Месть Масамунэ",
                      "Непутёвый ученик в школе магии",
                      "Маг на полную ставку",
                      "Этот замечательный мир",
                      "Моб Психо 100",
                      "Сага о Винланде",
                      "Ох, уж этот экстрасенс Сайки Кусуо",
                      "Башня Бога",
                      "Князь тьмы меняет профессию",
                      "Пламенная бригада пожарных",
                      "Добро пожаловать в ад, Ирума",
                      "Госпожа Кагуя",
                      "24 округ Токио"]
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
            name = arg.find('a').string

            returnString += "-"
            returnString += arg.find('a').string
            returnString += "\n"
            s.add(name)
    return returnString
