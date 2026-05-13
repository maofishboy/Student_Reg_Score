from Command.AddStu import AddStu
from Command.DelStu import DelStu
from Command.ModifyStu import ModifyStu
from Command.PrintAll import PrintAll
from Command.QueryStu import QueryStu
from SocketServer.SocketServer import SocketServer
from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer

action_list = {
    "add": AddStu, 
    "query": QueryStu,
    "delete": DelStu, 
    "modify": ModifyStu, 
    "show": PrintAll
}

class StudentManager:
    def manager_execute(self, command, parameters):
        result = action_list[command]().execute(parameters)
        return result

def main():
    DBConnection.db_file_path = "student_dict.db"
    DBInitializer().execute()
    student_manager = StudentManager()
    server = SocketServer(student_manager)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")

main()