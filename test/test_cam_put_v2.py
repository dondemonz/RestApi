import requests
from model.json_check import *
from model.input_data import *
import time



def test_PutV2CamerasCode200():
    data = {"name": camId}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"", headers=headers, data=json.dumps(dict(data)), auth=auth)
    # if_there_is_no_json(response)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_PutV2CamerasCode401():
    data = {"name": camId}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/"+camId+"", headers=headers, data=json.dumps(dict(data)), auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_PutV2CamerasCode404():
    data1 = "Camera 0 not found."
    data = {"name": camId}
    response = requests.put(url="http://" + slave_ip + ":"+restPort+"/api/v2/cameras/0", headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["message"]
    assert data1 == n




