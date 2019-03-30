from model.input_data import *

def test_delete_environment(fix):
    fix.send_event(message="CORE||DELETE_OBJECT|objtype<PERSON>,objid<1.999>".encode("utf-8"))
    fix.send_event(message="CORE||DELETE_OBJECT|objtype<DEPARTMENT>,objid<1.999>".encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<RTSP_SERVER>,objid<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<ARCH_CNV>,objid<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<EVENT_FILTER>,objid<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<IMAGE_EXPORT>,objid<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<HTTP_EVENT_PROXY>,objid<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<REST_API>,objid<"+objId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<GRABBER>,objid<"+camId+">").encode("utf-8"))
    fix.send_event(message=("CORE||DELETE_OBJECT|objtype<GRABBER>,objid<"+camId2+">").encode("utf-8"))