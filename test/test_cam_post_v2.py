import requests
from model.json_check import *
from model.input_data import *
import time
import datetime as dt


def test_MoveV2CamerasCode200():
    data = "success"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/move?pan_speed=10&tilt_speed=-10&zoom_speed=0", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["status"]
    assert data == n


    response1 = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/move?pan_speed=0tilt_speed=0&zoom_speed=0", auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    body1 = json.dumps(response.json())
    data3 = json.loads(body1)
    n = data3["status"]
    assert data == n


def test_MoveV2CamerasPanCode400():
    data = "Incorrect parameter:pan_speed, value:a"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/move?pan_speed=a&tilt_speed=-10&zoom_speed=0", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n


def test_MoveV2CamerasTiltCode400():
    data = "Incorrect parameter:tilt_speed, value:a"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/move?pan_speed=0&tilt_speed=a&zoom_speed=0", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n


def test_MoveV2CamerasZoomCode400():
    data = "Incorrect parameter:zoom_speed, value:a"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/move?pan_speed=0&tilt_speed=0&zoom_speed=a", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n


def test_MoveV2CamerasCode401():
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/move?pan_speed=10&tilt_speed=-10&zoom_speed=0", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_MoveV2CamerasCode404():
    data = "Camera 0 not found."
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/0/ptz/move?pan_speed=10&tilt_speed=-10&zoom_speed=0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n


# Управление PTZ, команда PRESET_RECALL
def test_PresetV2CamerasCode200():
    data = "success"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/presets/recall?preset=0&pt_speed=0", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["status"]
    assert data == n

def test_PresetV2CamerasCode400():
    data = "Incorrect parameter:preset, value:a"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/presets/recall?preset=a&pt_speed=0", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_PresetV2CamerasCode401():
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/presets/recall?preset=0&pt_speed=0", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_PresetV2CamerasCode404():
    data = "Camera 0 not found."
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/0/ptz/presets/recall?preset=0&pt_speed=0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Управление PTZ, команды PATROL и STOP
def test_PatrolAndStopV2CamerasCode200():
    data = "success"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/patrols/play?patrol=0", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

    response1 = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/patrols/stop", auth=auth)
    user_resp_code = "200"
    assert str(response1.status_code) == user_resp_code
    data1 = json.loads(body)
    n1 = data1["status"]
    assert data == n1


def test_PatrolV2CamerasCode400():
    data = "Incorrect parameter:patrol, value:a"
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/patrols/play?patrol=a", auth=auth)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_PatrolV2CamerasCode401():
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/patrols/play?patrol=0", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_PatrolV2CamerasCode404():
    data = "Camera 0 not found."
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/0/ptz/patrols/play?patrol=0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

def test_StopV2CamerasCode401():
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/ptz/patrols/stop", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_StopV2CamerasCode404():
    data = "Camera 0 not found."
    response = requests.post(url="http://" + slave_ip + ":8888/api/v2/cameras/0/ptz/patrols/stop", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n