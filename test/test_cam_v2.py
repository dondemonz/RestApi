import requests
from model.json_check import *
from model.input_data import *


# Запрос на получение настроек всех объектов CAM
def test_GetV2AllCamerasCode200():
    data = "success"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV2AllCamerasStatus401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


# Запрос на получение настроек объекта CAM
def test_GetV2CamerasByIdCode200():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV2CamerasByIdCode401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId, auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV2CamerasByIdCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

#Запрос на получение поля status объекта CAM
def test_GetV2CameraStatusCode200():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/status", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV2CameraStatusCode401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/status", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV2CameraStatusCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/0/status", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n


# Запрос на получение поля rtsp объекта CAM
def test_GetV2CameraRtspCode200():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/rtsp", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV2CameraRtspCode401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/rtsp", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV2CameraRtspCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/0/rtsp", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запрос на получение поля rtsp/live объекта CAM
def test_GetV2CameraRtspLiveCode200():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/rtsp/live", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV2CameraRtspLiveCode401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/rtsp/live", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV2CameraRtspLiveCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/0/rtsp/live", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запрос на получение поля rtsp/archive объекта CAM
def test_GetV2CameraRtspArchiveCode200():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/rtsp/archive", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV2CameraRtspArchiveCode401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/rtsp/archive", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV2CameraRtspArchiveCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/0/rtsp/archive", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n
