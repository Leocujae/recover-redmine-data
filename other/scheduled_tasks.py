
import json
from datetime import datetime, timedelta


def function(url='flattened_data_issues.json'):

 filter_data = [] 
 
 with open(url, 'r') as archivo_json:
    json_obj = json.load(archivo_json)
 
 for issue in json_obj:
    print(issue)
    filter_data.append(issue)
 filter_data.append({"count":len(filter_data)})
 
 print("SADSDA")
 return filter_data
function()