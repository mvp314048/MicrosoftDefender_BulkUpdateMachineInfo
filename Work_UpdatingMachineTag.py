#import csv
#import pyodbc
import json
import urllib.request
import urllib.parse
import urllib.error
import requests
import os
import re
from datetime import datetime

def __Convert__(string):
    li = list(string.split(" "))
    return li

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


#print(aadToken) #To Check the raw token value, for Debugging.



queryKQLAdd = open(
    r'C:\Users\ryanc\Documents\GitHub\MicrosoftDefender_BulkUpdateMachineInfo\---AdvancedHuntingScript\--AASIA\ListAIN(Bangalore)Machine.txt')  # To Open the AdvancedHunting script.
queryAdd = queryKQLAdd.read()
queryKQLAdd.close()

queryKQLRemoval = open(
    r'C:\Users\ryanc\Documents\GitHub\MicrosoftDefender_BulkUpdateMachineInfo\---AdvancedHuntingScript\--AASIA\ListAIN(Bangalore)MachineRemoval.txt')  # To Open the AdvancedHunting script.
queryRemoval = queryKQLRemoval.read()
queryKQLRemoval.close()


url = "https://api.securitycenter.microsoft.com/api/advancedqueries/run"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': "Bearer " + aadToken
}

data = json.dumps({ 'Query' : queryAdd }).encode("utf-8")

reqToAdd = urllib.request.Request(url, data, headers)
responseToAdd = urllib.request.urlopen(reqToAdd)
jsonResponseForAdd = json.loads(responseToAdd.read())
schemaForAdd = jsonResponseForAdd["Schema"]
resultsForAdd = jsonResponseForAdd["Results"]

data = json.dumps({ 'Query' : queryRemoval }).encode("utf-8")

reqToRemove = urllib.request.Request(url, data, headers)
responseToRemove = urllib.request.urlopen(reqToRemove)
jsonResponseForRemove = json.loads(responseToRemove.read())
schemaForRemove = jsonResponseForRemove["Schema"]
resultsForRemove = jsonResponseForRemove["Results"]


url = "https://api.securitycenter.microsoft.com/api/machines/AddOrRemoveTagForMultipleMachines"


# The Removing section begin from here.
print("------------ The removing job is starting -------------")
machineIdsValue = []
count = 0
Total = 0
for EveryEntry in resultsForRemove:
    __Convert__(EveryEntry["DeviceId"])

    if EveryEntry["DeviceId"] not in machineIdsValue:
        machineIdsValue.append(EveryEntry["DeviceId"])
        
        if len(machineIdsValue) == 495:
             
            body = {
                "Value" : "AIN(Bangalore)",
                "Action" : "Remove",
                "MachineIds" : machineIdsValue
            }        
            
            try:
                data = json.dumps(body).encode("utf-8")
                            
                req = urllib.request.Request(url, data, headers)
                response = urllib.request.urlopen(req)
                jsonResponse = json.loads(response.read())
                
                count = count+1
                print("The length of entries has reached the 495 limit. The removing job is performing the", count, "Times...")
                
                Total = Total + len(machineIdsValue)
                machineIdsValue.clear()
    
            except urllib.error.HTTPError as err:
                        
                if err.code == 400:
                    json_container = json.loads(str(err.read(), 'utf-8'))
                    
                    dictGet = json_container["error"]["message"]
                    dictSplit = dictGet.split()
                    dictSplit2 = str(dictSplit)
                    mixed_string = re.findall(r'\b\w+\b', dictSplit2)
                    subset = mixed_string[4:]      
                    
                    for errorEntry in subset:
                        if errorEntry in machineIdsValue:
                            machineIdsValue.remove(errorEntry)        
                            
                    body = {
                            "Value" : "AIN(Bangalore)",
                            "Action" : "Remove",
                            "MachineIds" : machineIdsValue
                    }     
                
                    data = json.dumps(body).encode("utf-8")
                    
                    req = urllib.request.Request(url, data, headers)
                    response = urllib.request.urlopen(req)
                    jsonResponse = json.loads(response.read())
                    
                    count = count+1
                    print("The length is", len(machineIdsValue), "after error handling. The removing job is performing the", count, "Times...")
                    
                    Total = Total + len(machineIdsValue)
                    machineIdsValue.clear()
                
if len(machineIdsValue) == 0:
        print ("The length is zero..., ending the removing job")

else:
    try:
        body = {
            "Value" : "AIN(Bangalore)",
            "Action" : "Remove",
            "MachineIds" : machineIdsValue
        }
        
      
        data = json.dumps(body).encode("utf-8")
                    
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        jsonResponse = json.loads(response.read())
        
        count = count+1
        print("The length is", len(machineIdsValue), ". The removing job is performing the", count, "Times...")
        
        Total = Total + len(machineIdsValue)
        machineIdsValue.clear()
    
    except urllib.error.HTTPError as err:
        
        if err.code == 400:
            json_container = json.loads(str(err.read(), 'utf-8'))
            
            dictGet = json_container["error"]["message"]
            dictSplit = dictGet.split()
            dictSplit2 = str(dictSplit)
            mixed_string = re.findall(r'\b\w+\b', dictSplit2)
            subset = mixed_string[4:]      
            
            for errorEntry in subset:
                if errorEntry in machineIdsValue:
                    machineIdsValue.remove(errorEntry)        
                    
            body = {
                    "Value" : "AIN(Bangalore)",
                    "Action" : "Remove",
                    "MachineIds" : machineIdsValue
            }     
    
            data = json.dumps(body).encode("utf-8")
            
            req = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(req)
            jsonResponse = json.loads(response.read())
            
            count = count+1
            print("The length is", len(machineIdsValue), "after error handling. The removing job is performing the", count, "Times...")
            
            Total = Total + len(machineIdsValue)
            machineIdsValue.clear()
            
print("The total length of removing is", Total)                        
        
# The Adding section begin from here.
print("------------ The adding job is starting -------------")
machineIdsValue = []
count = 0
Total = 0
for EveryEntry in resultsForAdd:
    __Convert__(EveryEntry["DeviceId"])

    if EveryEntry["DeviceId"] not in machineIdsValue:
        machineIdsValue.append(EveryEntry["DeviceId"])
        
        if len(machineIdsValue) == 495:
                   
            body = {
                "Value" : "AIN(Bangalore)",
                "Action" : "Add",
                "MachineIds" : machineIdsValue
            }
            
            
            try:
            
                data = json.dumps(body).encode("utf-8")
                            
                req = urllib.request.Request(url, data, headers)
                response = urllib.request.urlopen(req)
                jsonResponse = json.loads(response.read())
                
                count = count+1 
                print("The length of entries has reached the 495 limit. The adding job is performing the", count, "Times...")
                
                Total = Total + len(machineIdsValue)
                machineIdsValue.clear()
            
            except urllib.error.HTTPError as err:
    
                if err.code == 400:
                    json_container = json.loads(str(err.read(), 'utf-8'))
                    
                    dictGet = json_container["error"]["message"]
                    dictSplit = dictGet.split()
                    dictSplit2 = str(dictSplit)
                    mixed_string = re.findall(r'\b\w+\b', dictSplit2)
                    subset = mixed_string[4:]
                    
                    for errorEntry in subset:
                        if errorEntry in machineIdsValue:
                            machineIdsValue.remove(errorEntry)
                        
                    body = {
                            "Value" : "AIN(Bangalore)",
                            "Action" : "Add",
                            "MachineIds" : machineIdsValue
                    }                               
                    
                    data = json.dumps(body).encode("utf-8")
                    
                    req = urllib.request.Request(url, data, headers)
                    response = urllib.request.urlopen(req)
                    jsonResponse = json.loads(response.read())
                    
                    count = count+1
                    print("The length is", len(machineIdsValue), "after error handling. The adding job is performing the", count, "Times...")
                    
                    Total = Total + len(machineIdsValue)
                    machineIdsValue.clear()                      
            
if len(machineIdsValue) == 0:
    print ("The length is zero..., ending the adding job")            
        
else:
    try:
        body = {
            "Value" : "AIN(Bangalore)",
            "Action" : "Add",
            "MachineIds" : machineIdsValue
        }   
        
        data = json.dumps(body).encode("utf-8")
                    
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        jsonResponse = json.loads(response.read())
        
        count = count+1
        print("The length is", len(machineIdsValue), ". The adding job is performing the", count, "Times...")
        
        Total = Total + len(machineIdsValue)
        machineIdsValue.clear()
            
            
    except urllib.error.HTTPError as err:
        
        if err.code == 400:
            json_container = json.loads(str(err.read(), 'utf-8'))
            
            dictGet = json_container["error"]["message"]
            dictSplit = dictGet.split()
            dictSplit2 = str(dictSplit)
            mixed_string = re.findall(r'\b\w+\b', dictSplit2)
            subset = mixed_string[4:]
            
            for errorEntry in subset:
                if errorEntry in machineIdsValue:
                    machineIdsValue.remove(errorEntry)
                
            body = {
                    "Value" : "AIN(Bangalore)",
                    "Action" : "Add",
                    "MachineIds" : machineIdsValue
            }                               
            
            data = json.dumps(body).encode("utf-8")
            
            req = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(req)
            jsonResponse = json.loads(response.read())
                            
            count = count+1
            print("The length is", len(machineIdsValue), "after error handling. The adding job is performing the", count, "Times...")
            
            Total = Total + len(machineIdsValue)
            machineIdsValue.clear()
        
print("The total length of adding is", Total)