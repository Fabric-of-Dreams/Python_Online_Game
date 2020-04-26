import socket

class Network:
    def __init__(self):
        self.client = socket.socket()
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5556
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)

        id_and_color = self.client.recv(2048).decode()
        filtered_id_an_color = "".join(filter(lambda c: c not in ['(', "'", ',', ')'], id_and_color))
        id_and_color_list = filtered_id_an_color.split()

        self.id = id_and_color_list[0]
        self.color = (int(id_and_color_list[1]), int(id_and_color_list[2]), int(id_and_color_list[3]))

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


# Sends client's position to the server and get all player positions in response

    def send_pos(self, x, y):
        return self.send(self.id + ' ' + str(x) + ' ' + str(y))
