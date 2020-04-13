from fixture.load_dll import DllHelper
from model.input_data import *
import pytest
import winreg
import psutil
import shutil
import time
import os


@pytest.fixture
def fix(request):
    fixture = DllHelper()
    # функция disconnect передается в качестве параметра
    request.addfinalizer(fixture.disconnect)
    return fixture


@pytest.fixture(scope="session", autouse=True)
# Настройки в реестре для тестов GetV2CamImageCode412 и GetV2CamImageCode503:
# deltaArchive [REG_SZ] = 1 время ближайшего кадра в реестре
# downloadTImeout [REG_SZ] = 60 время ожидания запроса
def fix2(request):
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\ISS\\SecurOS\\Niss400\\ImageProcessor")
    winreg.SetValueEx(key, 'deltaArchive', 0, winreg.REG_SZ, '1')
    winreg.SetValueEx(key, 'downloadTimeout', 0, winreg.REG_SZ, '3')

    # Срубает video.exe для того, чтобы применились параметры реестра. !!!работает только если pycharm запущен от администратора!!!
    # Если нет шлюза и грабберов в системе, то video.exe нет и перезапускать его не надо, закомментирую эту часть пока
    # Примерно с 02.20 года начались проблемы с psutil.AccessDenied: программа пытается получить имя процесса и на какихто виндусовых процессах
    # падает, я отключил большинство фоновых приложений винды, стало луче, но падает теперь на других процессех. Решить пока не получается.
    """
    PROCNAME = "video.exe"
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
    time.sleep(5)
    print('\nSome recource')
    def fin():
        print('\nSome resource fin')
    request.addfinalizer(fin)
    return request
    """

#изначально проблем не было, но после включения доп процессоров (было 2 виртуальных добавил еще 2 виртуальных) начали периодические падения
#с treading долго копался, решил (вроде решил) слипами в 1 сек.
@pytest.fixture(scope="session", autouse=True)
def fix3(request):
    fix = DllHelper()
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<DEPARTMENT>,objid<"+departmentId+">,parent_id<1>,name<Test_Department>").encode("utf-8"))
    time.sleep(1)
    # если будет идеи, то сделать проверку на создание объектов IsObjectExists, но походу библиотека iidk не поддерживает
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<PERSON>,objid<1.999>,parent_id<"+personId+">,name<"+user+">,passwd2<"+password+">").encode("utf-8"))
    time.sleep(1)
    # fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<RIGHTS>,objid<1.2>,parent_id<1>,person.0<1.999>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<RTSP_SERVER>,objid<"+objId+">,parent_id<"+slave+">,name<Test_RTSP_Server>,").encode("utf-8"))  # "CAM.cam.count", 1, "CAM.cam.0", GetCamera()
    time.sleep(1)
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<RTSP_SERVER>,objid<" + objId + ">,parent_id<" + slave + ">,CAM.cam.count<1>,CAM.cam.0<" + camId + ">").encode("utf-8"))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<ARCH_CNV>,objid<"+objId+">,parent_id<"+slave+">,name<Test_Archive_Converter>").encode("utf-8"))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,name<Test_Event_Filter>").encode("utf-8"))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<IMAGE_EXPORT>,objid<"+objId+">,parent_id<"+slave+">,name<Test_Image_Processor>").encode("utf-8"))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<HTTP_EVENT_PROXY>,objid<"+objId+">,parent_id<"+slave+">,name<Test_HTTP_Event_Gate>,port<88>").encode("utf-8"))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<REST_API>,objid<"+objId+">,parent_id<"+slave+">,name<Test_RestAPI>").encode("utf-8"))
    # добовляем фильтр в рест для тестов протокола. В тестах есть дубликат, чтобы можно было запускать по кругу тесты без создания объектов. В конце тестов есть сброс фильтра в ресте.
    time.sleep(1)
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<REST_API>,objid<" + objId + ">,parent_id<" + slave + ">,event_filter_id<"+objId+">,port<"+restPort+">").encode("utf-8"))
    # указываем в фильтре разрешить все события, чтобы не повлияло на остальные тесты, если фильтр пуст - то события не проходят.
    time.sleep(1)
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<" + objId + ">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<>,EVENT.action.0<>").encode("utf-8")))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<GRABBER>,objid<"+objId+">,parent_id<"+slave+">,name<Grabber_for_delete>,type<Axis>").encode("utf-8"))  # type=Axis, т.к. без типа будет сильно грузиться система
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<CAM>,objid<"+objId+">,parent_id<"+objId+">,name<Cam_for_delete>").encode("utf-8"))
    #две камеры для тестов
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<GRABBER>,objid<" + camId + ">,parent_id<" + slave + ">,name<"+camName+">,type<ONVIF>,model<default>,format<H264>,ip<172.16.16.25>,user_name<service>,auth_crpt<ONAOECDBDDPNLNJBLOMAMOCDLEMNDOHN>").encode("utf-8"))  # type=Axis, т.к. без типа будет сильно грузиться система
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<CAM>,objid<" + camId + ">,parent_id<" + camId + ">,name<"+camName+">,telemetry_id<native>").encode("utf-8"))
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<GRABBER>,objid<" + camId2 + ">,parent_id<" + slave + ">,name<"+camName2+">,type<Axis>,model<M3027-PVE>,format<H264>,ip<172.16.16.10>,user_name<root>,auth_crpt<OLFNDJGNJHDLNPLJ>").encode("utf-8"))  # type=Axis, т.к. без типа будет сильно грузиться система
    time.sleep(1)
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<CAM>,objid<" + camId2 + ">,parent_id<" + camId2 + ">,name<"+camName2+">,telemetry_id<native>").encode("utf-8"))


    #создание папки для экспорта тестов cam_get_cam_image
    if not os.path.exists("C:\\export\\"):
        os.mkdir("C:\\export\\")
        print("Directory ", "C:\\export\\", " Created ")
    else:
        print("Directory ", "C:\\export\\", " already exists")
    time.sleep(5)
    print('\nSome recource')
    def fin():
        fix.send_event(message="CORE||DELETE_OBJECT|objtype<PERSON>,objid<1.999>".encode("utf-8"))
        time.sleep(1)
        fix.send_event(message="CORE||DELETE_OBJECT|objtype<DEPARTMENT>,objid<1.999>".encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<RTSP_SERVER>,objid<" + objId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<ARCH_CNV>,objid<" + objId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<EVENT_FILTER>,objid<" + objId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<IMAGE_EXPORT>,objid<" + objId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<HTTP_EVENT_PROXY>,objid<" + objId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<REST_API>,objid<" + objId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<GRABBER>,objid<" + camId + ">").encode("utf-8"))
        time.sleep(1)
        fix.send_event(message=("CORE||DELETE_OBJECT|objtype<GRABBER>,objid<" + camId2 + ">").encode("utf-8"))
        time.sleep(1)
        shutil.rmtree("C:\\export")
        print('\nSome resource fin')
        time.sleep(1)
        fix.disconnect()
    request.addfinalizer(fin)
    return request

