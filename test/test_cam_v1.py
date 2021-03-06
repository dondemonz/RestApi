import requests
from model.json_check import *
from model.input_data import *


# Запрос на получение настроек всех объектов CAM
def test_GetV1AllCamerasCode200():
    data = "success"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV1AllCamerasStatus401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


# Запрос на получение настроек объекта CAM
def test_GetV1CamerasByIdCode200():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV1CamerasByIdCode401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId, auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV1CamerasByIdCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

#Запрос на получение поля status объекта CAM
def test_GetV1CameraStatusCode200():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/status", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV1CameraStatusCode401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/status", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code



def test_GetV1CameraStatusCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/0/status", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запрос на получение поля rtsp объекта CAM
def test_GetV1CameraRtspCode200():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/rtsp", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV1CameraRtspCode401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/rtsp", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV1CameraRtspCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/0/rtsp", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запрос на получение поля rtsp/live объекта CAM
def test_GetV1CameraRtspLiveCode200():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/rtsp/live", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV1CameraRtspLiveCode401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/rtsp/live", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV1CameraRtspLiveCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/0/rtsp/live", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запрос на получение поля rtsp/archive объекта CAM
def test_GetV1CameraRtspArchiveCode200():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/rtsp/archive", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n

def test_GetV1CameraRtspArchiveCode401():
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/"+camId+"/rtsp/archive", auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code


def test_GetV1CameraRtspArchiveCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v1/cameras/0/rtsp/archive", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n
