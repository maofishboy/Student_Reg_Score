from Command.AddStu import AddStu
from Command.DelStu import DelStu
from Command.ModifyStu import ModifyStu
from Command.PrintAll import PrintAll
from Command.QueryStu import QueryStu
from SocketServer.SocketServer import SocketServer
from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from pathlib import Path
import sys
import time

action_list = {
    "add": AddStu, 
    "query": QueryStu,
    "delete": DelStu, 
    "modify": ModifyStu, 
    "show": PrintAll
}

class StudentManager:
    def manager_execute(self, command, parameters):
        if command not in action_list:
            return {"status": "Fail", "reason": f"Unknown command: {command}"}
        result = action_list[command]().execute(parameters)
        return result

def main():
    DBConnection.db_file_path = str(Path(__file__).resolve().parent / "student_dict.db")
    DBInitializer().execute()
    student_manager = StudentManager()
    server = SocketServer(student_manager)
    server.daemon = True
    server.serve()

    try:
        if sys.stdin and sys.stdin.isatty():
            while True:
                command = input()
                if command == "finish":
                    break
        else:
            while True:
                time.sleep(1)
    except (EOFError, KeyboardInterrupt):
        pass
    
    server.server_socket.close()
    print("leaving ....... ")


if __name__ == "__main__":
    main()
