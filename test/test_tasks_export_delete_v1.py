import requests
from model.json_check import *
from model.input_data import *
import time

def test_DeleteV1TaskCode200():
    data = {"camera": ""+camId+"", "from": "20000721T191940.000", "to": "20000728T191955.000"}
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/export/tasks/", headers=headers, data=json.dumps(dict(data)), auth=auth)
    body = json.dumps(response.json())
    data1 = json.loads(body)
    task_id = data1["data"]["id"]
    # print(task_id)
    time.sleep(3)
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/export/tasks/"+task_id, headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body1 = json.dumps(response.json())
    data2 = json.loads(body1)
    assert task_id == data2["data"]["id"]

def test_DeleteV1TaskCode401():
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/export/tasks/123", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_DeleteV1TaskCode404():
    data = "Unknown Task id:999"
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/export/tasks/999", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n