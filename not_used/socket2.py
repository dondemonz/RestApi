import socket

host = "127.0.0.1"
port = 1030
id = 1
myfunc = 0


sock = socket.socket()
# result = sock.connect_ex((host, port))
n = {id, myfunc, 0, 1, 0}
result = sock.connect_ex((host, port))

# result.send(str.encode(str(n)))
# sock.send(id)
print(result)

# data = sock.recv(1024)
sock.close()
if result:
    print("problem with socket!")
else:
    print("everything it's ok!")


"""
msg = 'Hello'
addr = (host, port, id)

def connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(host)
    sock.sendto(addr)


connection()

"""

"""
result = s.connect((host, port, id))
# s.close()
if result:
    print("problem with socket!")
else:
    print("everything it's ok!")
"""

"""
try:
    s.connect((host, port, id))
    # s.shutdown(2)
    print("Success connecting to ")
    print(host, " on port: ", str(port))
except socket.error as e:
    print("Cannot connect to ")
    print(host, " on port: ", str(port))
    print(e)
"""

"""
result = s.connect((host, port, id))
s.close()
if result:
    print("problem with socket!")
else:
    print("everything it's ok!")
"""


"""
    try:
    s.connect((host, port, id))
    # originally, it was
    # except Exception, e:
    # but this syntax is not supported anymore.
except Exception as e:
    print("something's wrong with %s:%d. Exception is %s" % (host, port, e))
finally:
    s.close()
"""