# https://www.boligsiden.dk/

import requests
import time
from datetime import datetime,timedelta
from plyer import notification
import json


#URL = f"https://api.prod.bs-aws-stage.com/search/cases?zipCodes=2300&addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page=100&page=1&sortAscending=true&sortBy=timeOnMarket"
URL = f"https://api.prod.bs-aws-stage.com/search/cases?addressTypes=villa%2Ccondo%2Cterraced+house%2Choliday+house%2Ccooperative%2Cfarm%2Chobby+farm%2Cfull+year+plot%2Cvilla+apartment%2Choliday+plot&per_page=50&page=1&sortAscending=true&sortBy=timeOnMarket"
header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
result = requests.get(URL, headers=header)
#If the response is 200 then proceed
if result.ok:
    response_json = result.json()
    print(len(response_json['cases']))
    print(response_json['totalHits'])
else:
    print("No Response")
    