import socket

class Network:
    def __init__(self):
        self.client = socket.socket()
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5556
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.id = self.client.recv(2048).decode()
        print('id =', self.id)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


# Sends client's position to the server

    def sendPos(self, x, y):
        self.send(self.id + ' ' + str(x) + ' ' + str(y))