import requests
from model.json_check import *
from model.input_data import *


# Запрос на получение настроек всех объектов CAM
def test_GetV2AllCamerasCode200():
    data = "success"
    # "%23" заменяет символ # для удаленных систем
    response = requests.get(url="http://"+slave_ip+":"+restPort+"/api/v2/cameras/1%231", auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["status"]
    assert data == n

