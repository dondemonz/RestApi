import requests
from model.json_check import *
from model.input_data import *

def test_DeleteV2CamerasCode200():
    data = {"status": "success"}
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+objId+"", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    assert data == data1

def test_DeleteV2CamerasCode401():
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+objId+"", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_DeleteV2CamerasCode404():
    data = "Camera "+objId+" not found."
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+objId+"", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test123(fix):
    print("123")