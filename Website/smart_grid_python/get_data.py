import json
import requests
import sqlite3

def get_Resident_App_format(Resident):
    url = 'http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid/Users/'+Resident+'/Appliance_desc/la'
    headers = {
        'X-M2M-Origin': 'admin:admin',
        'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    return response["m2m:cin"]["con"]


def get_Resident_status(Resident):
    url = 'http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid/Users/'+Resident+'/All_status/la'
    headers = {
        'X-M2M-Origin': 'admin:admin',
        'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    return response["m2m:cin"]["con"]


def get_appliance_format(Resident, Appliance):
    url = 'http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid/Users/'+Resident+'/Appliances/'+Appliance+'/Descriptor/la'
    headers = {
        'X-M2M-Origin': 'admin:admin',
        'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    return response["m2m:cin"]["con"]


def get_appliance_data(Resident, Appliance, App_no):
    url = 'http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid/Users/'+Resident+'/Appliances/'+Appliance+'/'+App_no+'/la'
    headers = {
        'X-M2M-Origin': 'admin:admin',
        'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    if response:
        response = json.loads(response.text)
    print(response)
    format  = get_appliance_format(Resident, Appliance).replace("[","").replace("]","")
    format = format.split(",")
    return format, response
