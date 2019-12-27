import requests
from model.json_check import *
from model.input_data import *
import time

def test_GetV2AbsoluteCoordinatesCode200():
    data = "success"
    time.sleep(3)
    response = requests.get(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/"+camId+"/ptz/status", auth=auth)
    time.sleep(1)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV2AbsoluteCoordinatesCode401():
    time.sleep(3)
    response = requests.get(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/" + camId + "/ptz/status", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_GetV2AbsoluteCoordinatesCode404():
    time.sleep(3)
    data = "Unknown CAM id:0"
    response = requests.get(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/0/ptz/status", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_PostV2AbsoluteCoordinatesCode200():
    data = "success"
    time.sleep(3)
    response = requests.post(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/"+camId+"/ptz/move_abs?pan_position=1&tilt_position=1&zoom_position=1", auth=auth)
    time.sleep(2)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_PostV2AbsoluteCoordinatesCode401():
    time.sleep(3)
    response = requests.post(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/" + camId + "/ptz/move_abs?pan_position=1&tilt_position=1&zoom_position=1", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_PostV2AbsoluteCoordinatesCode404():
    time.sleep(3)
    data = "Camera 0 not found."
    response = requests.post(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/0/ptz/move_abs?pan_position=1&tilt_position=1&zoom_position=1", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_PostV2AbsoluteCoordinatesCode400():
    time.sleep(3)
    data = "Missed required parameter:tilt_position"
    response = requests.post(url="http://" + slave_ip + ":" + restPort + "/api/v2/cameras/" + camId + "/ptz/move_abs?pan_position=1&zoom_position=1", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n
