from threading import Thread
import socket
import json

host = "127.0.0.1"
port = 20001

class SocketServer(Thread):
    def __init__(self, student_manager):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.student_manager = student_manager

    def serve(self):
        self.start()

    def run(self):
        while True:
            try:
                connection, address = self.server_socket.accept()
                print("{} connected".format(address))
                self.new_connection(connection=connection,
                                    address=address)
            except Exception as e:
                pass


    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
            except Exception as e:
                keep_going = False
            else:
                if not message:
                    keep_going = False
                    continue
                message = json.loads(message)
                print(message)
                print(f"    server received: {message} from {address} ")
                result = self.student_manager.manager_execute(message['command'], message['parameters'])
                connection.send(json.dumps(result).encode())
        
        connection.close()
        print("{} close connection".format(address))