"""Test class for HTTP authentication method. Only for test purposes."""

import requests
import json
import pandas as pd
from requests.auth import HTTPBasicAuth


def auth_api_back(username, password):
    res = requests.get('https://api.quickbutik.com/v1/products', auth=HTTPBasicAuth(username, password))
    print(res.status_code)
    if res.status_code == 200:
        print("Authentication completed.")
        #openFile()
    else:
        print("Wrong authentication: response code", res.status_code)


def openFile():
    pdPath = r"C:\Users\angel\Downloads\Eliza tian.csv"

    data = pd.read_csv(pdPath)
    print(data)

    skuNumber = data.SKU
    title = data.PRODUKTTITEL
    description = data.PRODUKTBESKRIVNING
    price = data.PRIS

    print(skuNumber)
    print(title)
    print(description)
    for i in description:
        print(i)

auth_api_back(input("user name:"), input("password"))