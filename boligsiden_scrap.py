# https://www.boligsiden.dk/
from datetime import datetime
from pydoc import describe
import requests
import time
from datetime import datetime,timedelta
from plyer import notification
import json

from db.db import Database

db = Database()

def get_boligsiden_total_count(city_url):
    URL = "https://api.prod.bs-aws-stage.com/search/cases?municipalities={}&addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page=50&page=1&sortAscending=true&sortBy=timeOnMarket".format(city_url)
    #URL = "https://api.prod.bs-aws-stage.com/search/cases?cities={}&addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page=50&page=1&sortAscending=true&sortBy=timeOnMarket".format(city_url)
    header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    result = requests.get(URL, headers=header)
    #If the response is 200 then proceed
    if result.ok:
        response_json = result.json()
        return response_json['totalHits']
    else:
        return -1   

def scrap_from_boligsiden_page(city_url_method, page_method, per_page_method, listing_count):
    print('City: {}, page: {}, per page: {}, total listings: {}'.format(city_url_method, page_method, per_page_method, listing_count))
    URL = "https://api.prod.bs-aws-stage.com/search/cases?municipalities={}&addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page={}&page={}&sortAscending=true&sortBy=timeOnMarket".format(city_url_method, per_page_method, page_method)
    #URL = "https://api.prod.bs-aws-stage.com/search/cases?cities={}&addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page={}&page={}&sortAscending=true&sortBy=timeOnMarket".format(city_url_method, per_page_method, page_method)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    result = requests.get(URL, headers = header)
    #If the response is 200 then proceed
    if result.ok & ( result is not None):
        response_json = result.json()
        for case in result.json().get('cases'):
            # Populate the values for the case
            id = '{}-{}'.format(case.get('caseID'), case.get('priceCash'))
            caseId = case.get('caseID')
            company = case['realtor'].get('name')
            longitude = case['coordinates'].get('lon')
            latitude = case['coordinates'].get('lat')
            coordinate_type = case['coordinates'].get('type')
            street_name =  case['address'].get('roadName')
            house_nr = case['address'].get('houseNumber')
            floor = case['address'].get('floor')
            postcode = case['address'].get('zipCode')
            city = case['address'].get('cityName')
            area = case.get('weightedArea')
            if area is None:
                area = case.get('housingArea')
            price = case.get('priceCash')
            rooms = case.get('numberOfRooms')
            daysOnMarket = case.get('daysOnMarket')
            property_type = case.get('addressType')
            description_title = case.get('descriptionTitle')
            description_body = case.get('descriptionBody')
            date = datetime.today().strftime('%Y-%m-%d')
            
            db.insert(id, caseId, company, longitude, latitude, coordinate_type, street_name, 
                    house_nr, floor, postcode, city, area, price, rooms, daysOnMarket, 
                    property_type, description_title, description_body, date) 

            
    else:
        print("No Response")

def scrap_boligsiden():    
    cities = ['K%C3%B8benhavn']
    #cities = ["K%C3%B8benhavn+S","K%C3%B8benhavn+%C3%98","K%C3%B8benhavn+V","K%C3%B8benhavn+K","K%C3%B8benhavn+N","K%C3%B8benhavn+SV","K%C3%B8benhavn+NV"]    
    per_page = 50
    for city_url in cities:
        listing_count = get_boligsiden_total_count(city_url)
        for page in range(1, int(listing_count/per_page) + 1):
            scrap_from_boligsiden_page(city_url, page, per_page, listing_count)
        last_page = int(listing_count/per_page)
        last_page_count = listing_count - (last_page * per_page)
        scrap_from_boligsiden_page(city_url, last_page + 1, last_page_count , listing_count)
        
        
count_before = db.get_count()
scrap_boligsiden()
db.to_csv("")
count_after = db.get_count()
if count_before == count_after:
    with open('log.txt', 'a') as f:
        f.write("On {} there were no new additions to DB \n".format(datetime.today().strftime('%Y-%m-%d')))
#    https://api.prod.bs-aws-stage.com/search/locations/cases?addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&text=k%C3%B8benhavn
#    https://api.prod.bs-aws-stage.com/search/cases?cities=K%C3%B8benhavn+S&addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page=50&page=1&sortAscending=true&sortBy=timeOnMarket