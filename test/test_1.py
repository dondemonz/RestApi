# Должен быть создан интерфейс iidk
# Должен быть пользователь с полными правами

from model.input_data import *


def test_create_environment(fix):
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<DEPARTMENT>,objid<"+departmentId+">,parent_id<1>,name<Test_Department>").encode("utf-8"))
    # если будет идеи, то сделать проверку на создание объектов IsObjectExists, но походу библиотека iidk не поддерживает
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<PERSON>,objid<1.999>,parent_id<"+personId+">,name<"+user+">,passwd<"+password+">").encode("utf-8"))
    # fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<RIGHTS>,objid<1.2>,parent_id<1>,person.0<1.999>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<RTSP_SERVER>,objid<"+objId+">,parent_id<"+slave+">,name<Test_RTSP_Server>,").encode("utf-8"))  # "CAM.cam.count", 1, "CAM.cam.0", GetCamera()
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<RTSP_SERVER>,objid<" + objId + ">,parent_id<" + slave + ">,CAM.cam.count<1>,CAM.cam.0<" + camId + ">").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<ARCH_CNV>,objid<"+objId+">,parent_id<"+slave+">,name<Test_Archive_Converter>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">,parent_id<1>,name<Test_Event_Filter>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<IMAGE_EXPORT>,objid<"+objId+">,parent_id<"+slave+">,name<Test_Image_Processor>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<HTTP_EVENT_PROXY>,objid<"+objId+">,parent_id<"+slave+">,name<Test_HTTP_Event_Gate>,port<88>").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<REST_API>,objid<"+objId+">,parent_id<"+slave+">,name<Test_RestAPI>").encode("utf-8"))
    # добовляем фильтр в рест для тестов протокола. В тестах есть дубликат, чтобы можно было запускать по кругу тесты без создания объектов. В конце тестов есть сброс фильтра в ресте.
    fix.send_event(message=("CORE||UPDATE_OBJECT|objtype<REST_API>,objid<" + objId + ">,parent_id<" + slave + ">,event_filter_id<"+objId+">").encode("utf-8"))
    # указываем в фильтре разрешить все события, чтобы не повлияло на остальные тесты, если фильтр пуст - то события не проходят.
    fix.send_event(message=(("CORE||UPDATE_OBJECT|objtype<EVENT_FILTER>,objid<" + objId + ">,parent_id<1>,EVENT.action.count<1>,EVENT.type.count<1>,EVENT.id.count<1>,EVENT.rule.count<1>,EVENT.rule.0<1>,EVENT.id.0<>,EVENT.type.0<>,EVENT.action.0<>").encode("utf-8")))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<GRABBER>,objid<"+objId+">,parent_id<"+slave+">,name<Grabber_for_delete>,type<Axis>").encode("utf-8"))  # type=Axis, т.к. без типа будет сильно грузиться система
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<CAM>,objid<"+objId+">,parent_id<"+objId+">,name<Cam_for_delete>").encode("utf-8"))
    #две камеры для тестов
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<GRABBER>,objid<" + camId + ">,parent_id<" + slave + ">,name<"+camName+">,type<Axis>,model<default>,format<H264>,ip<172.16.16.10>,user_name<root>,auth_crpt<OLFNDJGNJHDLNPLJ>").encode("utf-8"))  # type=Axis, т.к. без типа будет сильно грузиться система
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<CAM>,objid<" + camId + ">,parent_id<" + camId + ">,name<"+camName+">").encode("utf-8"))
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<GRABBER>,objid<" + camId2 + ">,parent_id<" + slave + ">,name<"+camName2+">,type<Axis>,model<default>,format<H264>,ip<172.16.16.10>,user_name<root>,auth_crpt<OLFNDJGNJHDLNPLJ>").encode("utf-8"))  # type=Axis, т.к. без типа будет сильно грузиться система
    fix.send_event(message=("CORE||CREATE_OBJECT|objtype<CAM>,objid<" + camId2 + ">,parent_id<" + camId2 + ">,name<"+camName2+">").encode("utf-8"))

    # как проверить есть ли в системе рест и включить ему фильтр или удалить и создать свой рест?
    # fix.send_event(message=("CORE||DELETE_OBJECT|objtype<REST_API>,objid<*>").encode("utf-8"))


"""
def test_test(fix):
    fix.connect_to_dll()
    i = 0
    while i < 100:
        fix.send_event(("CAM|202|ARCH_GET_RECORDS").encode("utf-8")) yu
    i += 1
"""


    # fix.send_event(message=("CORE||CREATE_OBJECT|objtype<ACTIVEX>,objid<" + objId + ">,parent_id<" + slave + ">,name<Test_IIDK_Interface>").encode("utf-8"))
