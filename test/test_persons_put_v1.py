import requests
from model.json_check import *
from model.input_data import *
import time

#Изменение настроек объекта PERSONS
def test_PutV1PersonsCode200():
    data = {"name": personName}
    response = requests.put(url="http://" + slave_ip + ":8888/api/v1/persons/"+personId+"", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["name"]
    assert personName == n

def test_PutV1PersonsCode401():
    data = {"name": personName}
    response = requests.put(url="http://" + slave_ip + ":8888/api/v1/persons/"+personId+"", headers=headers, data=json.dumps(dict(data)), auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_PutV1PersonsCode404():
    data = {"name": personName}
    data1 = "Person 0 not found."
    response = requests.put(url="http://" + slave_ip + ":8888/api/v1/persons/0", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["message"]
    assert data1 == n

