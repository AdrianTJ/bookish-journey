# General Imports
import string
import requests
import json
from google.cloud import storage
import csv
from datetime import datetime, timedelta


#function that receives a set of drinks with their ingredients and stores them in google cloud as JSON type files
def write_blob_from_list(list, bucket, path_auth):

#inputs:
#list: data-frame with the information of the ingredients of each drink
#bucket: the name of the reserved space to store information in google cloud
#path_auth: the path of the security file
    
    client = storage.Client.from_service_account_json(path_auth)
    gcs_bucket = client.get_bucket(bucket)
    for letter in list:
        path = f"cocktails/{letter[0]}/ingredients.json"
        blob = gcs_bucket.blob(path)
        blob.upload_from_string(data=json.dumps(letter[1]), content_type='application/json')
    print(f"Writing {len(letter)} rows to gs://{bucket}/{path}")


# Function that connects to the cocktail api and retrieves all the recipes in alphabetical order.    
def get_drink(bucket, key, path_auth):
#bucket: the name of the reserved space to store information in google cloud
#key: reserved code that allows extracting information from the api
#path_auth: the path of the security file   

#This section generates all the instructions to connect and extract from the api using the key first letter of the name of the drink
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)  
    cocktails_key = key
    base_url = "https://www.thecocktaildb.com/api/"
    json_api = 'json/v1/'
    auth = f'{cocktails_key}'
    request_bodies = []
    for letter in alphabet_list:
        request_bodies.append(base_url + json_api + auth + f"/search.php?f={letter}")

#the connection to the api is established and the drinks are extracted in JSON format
    data = []
    for request in request_bodies:
        data.append(requests.get(request).json())

#the relevant information is extracted from the JSON, the labels that are not valid for bigquery are modified
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
    
#the function is commanded to be executed    
    write_blob_from_list(drink, bucket, path_auth)