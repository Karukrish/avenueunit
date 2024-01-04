import requests
import json
from jsonpath_ng import jsonpath, parse
import pytest
from dotenv import load_dotenv
import os
import logging
from utlities import Readconfig
import testdata
from uuid import UUID
import excelutil



#Login to the hire

@pytest.fixture(scope= 'class')
def login(request: pytest.FixtureRequest):
  try:
   
    #load_dotenv()

  # agenname = os.getenv('agentname')
  # password = os.getenv('password')
    #device = os.getenv('device')

    agenname = Readconfig.getusername()
    password = Readconfig.getpassword()
    #device = Readconfig.getdevice()


    url = 'https://gateway.ss.dev/signin/public/api'

    data = {
      "operationName": "SignIn",
      "variables": {
        "input": {
          "device": {
            "id": '890ff2c4-31f6-4c7c-9a15-dfba8450704e',
            "name": "Windows",
            "client": "Web"
          },
          "email": agenname,
          "password": password
        }
      },
      "query": "mutation SignIn($input: InputSignIn!) {\n  signIn(input: $input) {\n    id\n    user {\n      id\n      firstName\n      lastName\n      email\n      profileUri\n      token {\n        type\n        value\n        __typename\n      }\n      __typename\n    }\n    organizations {\n      id\n      name\n      label\n      lastActiveTimestamp\n      product {\n        id\n        name\n        __typename\n      }\n      token {\n        type\n        value\n        __typename\n      }\n      status\n      __typename\n    }\n    resetPasswordToken\n    __typename\n  }\n}"
    }

    headers = {
            'Content-Type': 'application/json'
            } 
    payload = json.dumps(data) #convert python payload to json support
    response = requests.request('POST',url,headers=headers,data=payload)
    #if 'Invalid credentials' in response.text:
     #  print (response.message)

    if response.status_code == 200:
         finalresponse = response.json()
         output = json.dumps(finalresponse) #these two line are required to convert in proper json format so I can find json path using pathfinder on google
         print(type(output))
         print("output: ", output)
         jsonpath_expr = parse('$.data.signIn.organizations[0].token.value') 
         token = [match.value for match in jsonpath_expr.find(finalresponse)]
         print('Token is'.join(token))
         request.cls.token ='-'. join(token)
 
    else :
        print('Received error in Login API',response.status_code)

  except Exception as e:
    print(f'Exception occured in login API {e}')

    
      

    


'''
@pytest.fixture()
def loggin(user,passord,request):
    url = 'https://gateway.ss.dev/signin/public/api'

    data = {
        "operationName": "SignIn",
        "variables": {
            "input": {
            "device": {
                "id": '9199371f-3f93-4f68-a9fa-f20d86fa917d',
                "name": "Windows",
                "client": "Web"
            },
            "email": user,
            "password": passord
            }
        },
        "query": "mutation SignIn($input: InputSignIn!) {\n  signIn(input: $input) {\n    id\n    user {\n      id\n      firstName\n      lastName\n      email\n      profileUri\n      token {\n        type\n        value\n        __typename\n      }\n      __typename\n    }\n    organizations {\n      id\n      name\n      label\n      lastActiveTimestamp\n      product {\n        id\n        name\n        __typename\n      }\n      token {\n        type\n        value\n        __typename\n      }\n      status\n      __typename\n    }\n    resetPasswordToken\n    __typename\n  }\n}"
        }

    headers = {
                'Content-Type': 'application/json'
                } 
    payload = json.dumps(data) #convert python payload to json support
    response = requests.request('POST',url,headers=headers,data=payload)
    if 'Invalid credentials' in response.text:
        print (response.text)

    elif response.status_code == 200:
            finalresponse = response.json()
            output = json.dumps(finalresponse) #these two line are required to convert in proper json format so I can find json path using pathfinder on google
            #print(type(output))
            print("output: ", output)
            jsonpath_expr = parse('$.data.signIn.organizations[0].token.value') 
            token = [match.value for match in jsonpath_expr.find(finalresponse)]
            print('Token is'.join(token))
            request.cls.token ='-'. join(token)
    
    else :
            print('Received error in Login API',response.status_code)

filepath = ('latest.xlsx')     
maxrow = excelutil.getrowcount(filepath,'Sheet1')
print(maxrow)
for r in range(2,maxrow+1):
            user = excelutil.readData(filepath,'Sheet1',r,2)
            passord  = excelutil.readData(filepath,'Sheet1',r,3)
            print(user)
            print(passord)
            login(user,passord)
'''
 
 



