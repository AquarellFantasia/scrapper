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

def get_boligsiden_total_count():
    URL = f"https://api.prod.bs-aws-stage.com/search/cases?addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page=50&page=1&sortAscending=true&sortBy=timeOnMarket"
    header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    result = requests.get(URL, headers=header)
    #If the response is 200 then proceed
    if result.ok:
        response_json = result.json()
        return response_json['totalHits']
    else:
        return -1   
        
def scrap_boligsiden():        
    listing_count = get_boligsiden_total_count()
    print('############################################################')
    print('Total count of listings found today: {}\n'.format(listing_count))
    print('Totatal database entries before scrapping: {}\n'.format(db.get_count()))
    print('############################################################')
    for page in range(1, int(listing_count/1000)):
        
        print('{}%\n'.format((page/(listing_count/1000))*100))
        
        URL = "https://api.prod.bs-aws-stage.com/search/cases?addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page={}&page={}&sortAscending=true&sortBy=timeOnMarket".format(1000, page)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        result = requests.get(URL, headers=header)
        #If the response is 200 then proceed
        if result.ok:
            response_json = result.json()
            for case in result.json()['cases']:
                
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
            
    print('############################################################')
    print('Totatal database entries after scrapping: {}'.format(db.get_count())) 
    print('############################################################')  
        
        
# def scrap_boligsiden2():        
#     listing_count = get_boligsiden_total_count()
#     page = 1
#     URL = "https://api.prod.bs-aws-stage.com/search/cases?addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page={}&page={}&sortAscending=true&sortBy=timeOnMarket".format(20, page)
#     header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
#     result = requests.get(URL, headers=header)
#     #If the response is 200 then proceed
#     if result.ok:
#         response_json = result.json()
#         for case in result.json()['cases']:
            
#             # Populate the values for the case
#             id = '{}-{}'.format(case.get('caseID'), case.get('priceCash'))
#             caseId = case.get('caseID')
#             company = case['realtor'].get('name')
#             longitude = case['coordinates'].get('lon')
#             latitude = case['coordinates'].get('lat')
#             coordinate_type = case['coordinates'].get('type')
#             street_name =  case['address'].get('roadName')
#             house_nr = case['address'].get('houseNumber')
#             floor = case['address'].get('floor')
#             postcode = case['address'].get('zipCode')
#             city = case['address'].get('cityName')
#             area = case.get('weightedArea')
#             price = case.get('priceCash')
#             rooms = case.get('numberOfRooms')
#             daysOnMarket = case.get('daysOnMarket')
#             property_type = case.get('addressType')
#             description_title = case.get('descriptionTitle')
#             description_body = case.get('descriptionBody')
            
            
#             print('-----------------------------------------------------')
#             print('id: {},company:{},longitude:{},latitude:{},coordinate_type:{},street_name:{},house_nr:{},floor:{},postcode:{},city:{},area:{},price:{},rooms:{},daysOnMarket:{},property_type:{},description_title:{},description_body:{}'.format(id, company, longitude, latitude, coordinate_type, street_name, 
#                         house_nr, floor, postcode, city, area, price, rooms, daysOnMarket, 
#                         property_type, description_title, description_body))
#             print('-----------------------------------------------------')
#             db.insert(id, company, longitude, latitude, coordinate_type, street_name, 
#                         house_nr, floor, postcode, city, area, price, rooms, daysOnMarket, 
#                         property_type, description_title, description_body)
        

#     else:
#         print("No Response")
  
scrap_boligsiden()


    