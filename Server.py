import socket
from _thread import *
import sys

server = socket.gethostbyname(socket.gethostname())
port = 5556

new_client_id = 0
players_colors = [(150, 0, 50), (0, 50, 150), (50, 150, 0)]
players_positions = {}

s = socket.socket()

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)

print("Server Started")
print('Waiting for a connection')


def threaded_client(conn, new_client_id):
    player_color = players_colors[new_client_id % len(players_colors)]
    conn.send(str.encode(str(new_client_id) + ' ' + str(player_color)))
    while True:
        try:
            raw_data = conn.recv(2048)

            if not raw_data:
                print('Disconnected')
                break
            else:
                data = raw_data.decode('utf-8')
                filtered_data = "".join(filter(lambda c: c not in ['(', "'", ',', ')'], data))
                data_list = filtered_data.split()
                id = int(data_list[0])
                color_r = data_list[1]
                color_g = data_list[2]
                color_b = data_list[3]
                x = data_list[4]
                y = data_list[5]
                players_positions[id] = (color_r, color_g, color_b, x, y)
                opponents_positions = players_positions.copy()
                opponents_positions.pop(id)

                opponents_positions_list = list(opponents_positions.values())
                if len(opponents_positions_list) != 0:
                    first_opp_pos = opponents_positions_list[0]
                    print('Sending: ', str(first_opp_pos))
                    conn.send(str.encode(str(first_opp_pos)))
                else:
                    conn.send(str.encode(' '))

        except:
            break

    players_positions.pop(new_client_id)
    print('Lost connection')
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ', addr)

    start_new_thread(threaded_client, (conn, new_client_id))

    new_client_id += 1
