import requests
from model.json_check import *
from model.input_data import *

# Запрос на получение настроек всех объектов PERSONS
def test_GetV1PersonCode200():
    data = "success"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/persons", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV1PersonCode401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/persons", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

# Запрос на получение настроек объекта PERSONS
def test_GetV1PersonByIdCode200():
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/"+personId+"", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert personId == n

def test_GetV1PersonByIdCode404():
    data = "Unknown PERSON id:0"
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n



def test_GetV1PersonByIdCode401():
    response = requests.get(url="http://" + slave_ip + ":"+restPort+"/api/v1/persons/0", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code
