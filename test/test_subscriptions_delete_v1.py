import requests
from model.json_check import *
from model.input_data import *

#Удаление подписки
def test_DeleteV1SubscriptionsCode200():
    data = {"callback": "http://localhost:9786/event?", "filter": {"action": "EVENT", "id": "777", "type": "TEST"}}
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/events/subscriptions", headers=headers, data=json.dumps(dict(data)), auth=auth)
    body = json.dumps(response.json())
    data1 = json.loads(body)
    subscriptionId = data1["data"]["id"]
    # print(subscriptionId)

    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/events/subscriptions/"+subscriptionId, auth=auth)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    body1 = json.dumps(response.json())
    data2 = json.loads(body1)
    assert subscriptionId == data2["data"]["id"]

def test_DeleteV1SubscriptionsCode401():
    data = {"callback": "http://localhost:9786/event?", "filter": {"action": "EVENT", "id": "777", "type": "TEST"}}
    response = requests.post(url="http://" + slave_ip + ":"+restPort+"/api/v1/events/subscriptions", headers=headers, data=json.dumps(dict(data)), auth=auth)
    body = json.dumps(response.json())
    data1 = json.loads(body)
    subscriptionId = data1["data"]["id"]
    # print(subscriptionId)

    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/events/subscriptions/"+subscriptionId, auth=("", ""))
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_DeleteV1SubscriptionsCode404():
    data = "Unknown Subscription id:0"
    response = requests.delete(url="http://" + slave_ip + ":"+restPort+"/api/v1/events/subscriptions/0", auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n
