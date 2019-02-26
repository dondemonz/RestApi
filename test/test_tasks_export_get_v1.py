import requests
from model.json_check import *
from model.input_data import *

def test_GetV1TasksCode200():
    data = "success"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v1/export/tasks", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV1TasksCode401():
    response = requests.get(url="http://" + slave_ip + ":8888/api/v1/export/tasks", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

# Запрос на получение информации по несуществующей задаче
def test_GetV1TaskByIdCode404():
    data = "Unknown Task id:999"
    response = requests.delete(url="http://" + slave_ip + ":8888/api/v1/export/tasks/999", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n