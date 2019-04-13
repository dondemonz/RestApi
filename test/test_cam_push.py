import requests
from model.json_check import *
from model.input_data import *

def test_PutV2CamerasCode200():
    data = {"name": ""+camId+""}
    response = requests.put(url="http://"+slave_ip+":"+restPort+"/api/v2/cameras/"+camId, headers=headers, data=json.dumps(dict(data)), auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["data"]["id"]
    assert camId == n
