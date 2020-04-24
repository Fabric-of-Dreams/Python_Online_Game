import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5556

new_client_id = 0
players_positions = {}

s = socket.socket()

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)

print("Server Started")
print('Waiting for a connection')

def process_data(raw_data):
    data = raw_data.decode('utf-8')
    print('Received: ', data)
    data_arr = data.split()
    id = int(data_arr[0])
    x = data_arr[1]
    y = data_arr[2]
    players_positions[id] = (x, y)
    # print(f'id = {id}, x = {x}, y = {y}')
    print(players_positions)


def threaded_client(conn, new_client_id):
    conn.send(str.encode(str(new_client_id)))
    reply = ''
    while True:
        try:
            raw_data = conn.recv(2048)
            reply = raw_data.decode('utf-8')

            if not raw_data:
                print('Disconnected')
                break
            else:
                process_data(raw_data)

                print('Sending: ', reply)

            conn.send(str.encode(reply))
        except:
            break

    print('Lost connection')
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ', addr)

    start_new_thread(threaded_client, (conn, new_client_id))

    new_client_id += 1
