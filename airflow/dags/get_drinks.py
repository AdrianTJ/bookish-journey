import string
import requests
import json
from google.cloud import storage
import csv
from datetime import datetime, timedelta


def write_blob_from_list(list, bucket, path_auth):
    client = storage.Client.from_service_account_json(path_auth)
    gcs_bucket = client.get_bucket(bucket)
    for letter in list:
        path = f"cocktails/{letter[0]}/ingredients.json"
        blob = gcs_bucket.blob(path)
        blob.upload_from_string(data=json.dumps(letter[1]), content_type='application/json')
    print(f"Writing {len(letter)} rows to gs://{bucket}/{path}")

def get_drink(bucket, key, path_auth):
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)  
    cocktails_key = key
    base_url = "https://www.thecocktaildb.com/api/"
    json_api = 'json/v1/'
    auth = f'{cocktails_key}'
    request_bodies = []
    for letter in alphabet_list:
        request_bodies.append(base_url + json_api + auth + f"/search.php?f={letter}")
        
    data = []
    for request in request_bodies:
        data.append(requests.get(request).json())

    drink = []
    for letter in data:
        if letter['drinks'] != None: 
            for drinks in letter['drinks']:
                id= drinks['idDrink']
                dato=[id,drinks]
                drink_jaison = dato[1]
                drink_jaison["strInstructionsZH_HANS"] = drink_jaison["strInstructionsZH-HANS"]
                drink_jaison["strInstructionsZH_HANT"] = drink_jaison["strInstructionsZH-HANT"]
                del drink_jaison["strInstructionsZH-HANS"]
                del drink_jaison["strInstructionsZH-HANT"]
                dato[1] = drink_jaison
                drink.append(dato)
                
    write_blob_from_list(drink, bucket, path_auth)