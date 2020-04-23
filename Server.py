import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket()

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)

print("Server Started")
print('Waiting for a connection')

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                print('Disconnected')
                break
            else:
                print('Received: ', reply)
                print('Sending: ', reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print('Lost connection')
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ', addr)

    start_new_thread(threaded_client, (conn, ))