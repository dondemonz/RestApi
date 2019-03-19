import requests
from model.json_check import *
from model.input_data import *
import shutil
import time
import datetime as dt
import winreg
import psutil

# import grequests
# from threading import Thread
# from requests import get, post, put, patch, delete, options, head


# Запросы на получения кадра живого видео с камеры


# Настройки в реестре для тестов GetV2CamImageCode412 и GetV2CamImageCode503:
# deltaArchive [REG_SZ] = 1 время ближайшего кадра в реестре
# downloadTImeout [REG_SZ] = 60 время ожидания запроса
def test_create_key_and_pareams():   # создает параемтры в реестре, downloadTImeout 2 т.к. с 60 не проходит тест
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\ISS\\SecurOS\\Niss400\\ImageProcessor")
    winreg.SetValueEx(key, 'deltaArchive', 0, winreg.REG_SZ, '1')
    winreg.SetValueEx(key, 'downloadTimeout', 0, winreg.REG_SZ, '2')

# срубает video.exe для того, чтобы применились параметры реестра. !!!работает только если pycharm запущен от администратора!!!
def test_reload_video_exe():
    PROCNAME = "video.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
    time.sleep(5)

def test_GetV2CamLiveImageCode200():
    # data = "success"
    response = requests.get(url="http://"+slave_ip+":8888/api/v2/cameras/"+camId+"/image", auth=auth, stream=True)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code

    # контент картинки, почему то есть проблемы с сохранением файла при этом выводе
    # print(response.content)

    # сохранить картинку в файл
    with open(exportPath+'img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


    """
    # сразу показать картинку
    with io.BytesIO(response.content) as f:
        with Image.open(f) as img:
            img.show()
    """

def test_GetV2CamLiveImageCode401():
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image", auth=("", ""), stream=True)
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_GetV2CamLiveImageCode404_CamNotFound():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/0/image", auth=auth, stream=True)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запрос на получение масштабированного кадра живого видео с камеры
def test_GetV2CamLiveScaleImageCode200():
    # data = "success"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image?scale_y=500&scale_x=500", auth=auth, stream=True)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    # сохранить картинку в файл
    with open(exportPath+'img1.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def test_GetV2CamLiveScaleImageCode200WithOnlyX():
    # data = "success"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/45/image?scale_x=500", auth=auth, stream=True)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    # сохранить картинку в файл
    with open(exportPath+'img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def test_GetV2CamLiveScaleImageCode200WithOnlyY():
    # data = "success"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/45/image?scale_y=500", auth=auth, stream=True)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    # сохранить картинку в файл
    with open(exportPath+'img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def test_GetV2CamLiveScaleImageCode401():
    # data = "success"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image?scale_y=500&scale_x=500", auth=("", ""), stream=True)
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_GetV2CamLiveScaleImageCode404():
    data = "Unknown CAM id:0"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/0/image?scale_y=500", auth=auth, stream=True)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n

# Запросы на получение кадра с камеры
def test_GetV2CamImageCode200(fix):
    fix.send_react(("CAM|"+camId+"|REC").encode("utf-8"))
    time.sleep(1)
    # нужен ключ реестра deltaArchive который создается в первом тесте этого раздела
    m = dt.datetime.now()
    archtime = m.strftime("%Y%m%dT%H%M%S")
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|REC_STOP").encode("utf-8"))
    time.sleep(1)
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image/"+archtime, auth=auth, stream=True)
    user_resp_code = "200"
    assert str(response.status_code) == user_resp_code
    # print(response)
    # контент картинки, почему то есть проблемы с сохранением файла при этом выводе
    # print(response.content)

    # сохранить картинку в файл
    with open(exportPath+'img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def test_GetV2CamImageCode400_IncorrectTime():
    data1 = "time (2015-11-19T18:480:32) is not in valid format or incorrect. Expected format: yyyy-MM-dd hh:mm:ss[.zzz]"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image/2015-11-19T18:480:32", auth=auth, stream=True)
    user_resp_code = "400"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["message"]
    assert data1 == n

def test_GetV2CamImageCode401():
    m = dt.datetime.now()
    archtime = m.strftime("%Y-%m-%d %H:%M:%S")
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image/"+archtime, auth=("", ""), stream=True)
    user_resp_code = "401"
    assert str(response.status_code) == user_resp_code

def test_GetV2CamImageCode404_CamNotFound():
    data1 = "Unknown CAM id:0"
    m = dt.datetime.now()
    archtime = m.strftime("%Y-%m-%d %H:%M:%S")
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/0/image/" + archtime, auth=auth)
    user_resp_code = "404"
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data2 = json.loads(body)
    n = data2["message"]
    assert data1 == n

def test_GetV2CamImageCode412(fix):
    fix.send_react(("CAM|"+camId+"|REC").encode("utf-8"))
    time.sleep(1)
    fix.send_react(("CAM|"+camId+"|REC_STOP").encode("utf-8"))
    time.sleep(2)
    m = dt.datetime.now()
    archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # [:-3] убирает 3 последних символа
    data = "Ошибка получения изображения: Камера "+camId+": архив для " + archtime + " не найден"
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image/" + archtime, auth=auth, stream=True)
    user_resp_code = "412"
    # print(response)
    assert str(response.status_code) == user_resp_code
    body = json.dumps(response.json())
    data1 = json.loads(body)
    n = data1["message"]
    assert data == n


def test_GetV2CamImageCode503():
    time.sleep(5)
    i = 0
    while i < 50:
        m = dt.datetime.now()
        archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        try:
            response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image/" + archtime, auth=auth, timeout=0.01)
            response.raise_for_status()  # Raise error in case of failure Далее ловим ошибку, но продолжаем посылать запросы
        except requests.exceptions.RequestException:
            i += 1
    m = dt.datetime.now()
    archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    response = requests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/"+camId+"/image/" + archtime, auth=auth)
    user_resp_code = "503"
    assert str(response.status_code) == user_resp_code









"""
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)
"""

""" пример асинхронных запросов
    def test_GetV2CamImageCode503():
        reqs = []
        reqs2 = []
        i = 0
        while i < 50:
            m = dt.datetime.now()
            archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            grequests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/45/image/" + archtime, auth=auth,
                          timeout=0.5)
            i += 1
        time.sleep(2)
        m = dt.datetime.now()
        archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        reqs2.append(grequests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/45/image/" + archtime, auth=auth))

        response = grequests.map(reqs2)
        print(response)
"""
    # requests1 = (grequests.get(u+archtime, auth=auth) for u in urls)
    # responses = grequests.map(reqs)

    #json = [response.json() for response in responses]
    #pprint.pprint(json)


    # text = '\n'.join(response.text for response in responses)
    # print(text)


    #m = dt.datetime.now()
    #archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    #req = grequests.get(url="http://" + slave_ip + ":8888/api/v2/cameras/45/image/"+archtime, auth=auth)
    #response = grequests.map([req])
    #print(response)
    #user_resp_code = "503"
    #response_code_check(response, user_resp_code)
    #json_check(response)
    #body = json.dumps(response.json())
    #data2 = json.loads(body)
    #print(data2)
    #assert str(response.status_code) == user_resp_code


"""
request_methods = {
    'get': get,
    'post': post,
    'put': put,
    'patch': patch,
    'delete': delete,
    'options': options,
    'head': head,
}


def async_request(method, *args, callback=None, timeout=15, **kwargs):
    #Makes request on a different thread, and optionally passes response to a
    #`callback` function when request returns.
    
    method = request_methods[method.lower()]
    if callback:
        def callback_with_args(response, *args, **kwargs):
            callback(response)
        kwargs['hooks'] = {'response': callback_with_args}
    kwargs['timeout'] = timeout
    thread = Thread(target=method, args=args, kwargs=kwargs)
    thread.start()

def test_test2(fix):
    i = 0
    while i < 6:
        m = dt.datetime.now()
        archtime = m.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        async_request('get', 'http://172.16.1.131:8888/api/v2/cameras/45/image/'+archtime, auth=auth,
                      callback=lambda r: print(r.json()))
        i += 1
        print(i)
"""
