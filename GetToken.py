import json
import urllib.request
import urllib.parse
import requests
import csv
import os
import pyodbc
from datetime import datetime

tenantId = ''  # Paste your own tenant ID here
appId = ''  # Paste your own app ID here
appSecret = ''  # Paste your own app secret here
date = datetime.now().strftime("%Y_%m_%d")

url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenantId)

resourceAppIdUri = 'https://api.securitycenter.microsoft.com'

body = {
    'resource': resourceAppIdUri,
    'client_id': appId,
    'client_secret': appSecret,
    'grant_type': 'client_credentials'
}

data = urllib.parse.urlencode(body).encode("utf-8")

req = urllib.request.Request(url, data)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
aadToken = jsonResponse["access_token"]

print(aadToken) #To Check the raw token value, for Debugging.
