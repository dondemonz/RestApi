from parse import search


def check_event_gate_response(fix):
    n = fix.cb1.decode("utf-8")
    a = search('"action":"{}"', n)
    action = a.fixed[0]
    i = search('"id":"{}"', n)
    id = i.fixed[0]
    t = search('"type":"{}"', n)
    type = t.fixed[0]
    m = search('_method<{}>', n)
    method = m.fixed[0]
    p = search('_path</{}>', n)
    path = p.fixed[0]
    peer = search('_peer_address<{}>', n)
    peer_address = peer.fixed[0]
    return action, id, method, path, peer_address, type