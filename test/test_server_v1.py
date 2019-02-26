import requests
from model.json_check import *
from model.input_data import *

# выдает все объекты компьютер в системе
def test_GetV1AllServersCode200():
    data = "success"
    response = requests.get(url="http://"+slave_ip+":8888/api/v1/servers/", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

# выдает определенный объект компьютер
def test_GetV1ServersByIdCode200():
    data = "success"
    response = requests.get(url="http://"+slave_ip+":8888/api/v1/servers/"+slave, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

def test_GetV1ServerssByIdCode401():
    response = requests.get(url="http://"+slave_ip+":8888/api/v1/servers/"+slave, auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code



def test_GetV1ServerssByIdCode404():
    data = "Unknown server id:0"
    response = requests.get(url="http://"+slave_ip+":8888/api/v1/servers/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n
