from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from SocketClient .SocketClient import SocketClient
import json

class ExecuteSendCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data  # 接收字典格式的數據

    def run(self):
        client = SocketClient()
        try:
            client.send_command(self.data['command'], self.data['parameters'])
            response = client.wait_response()
            self.return_sig.emit(json.dumps(response))
        finally:
            client.close()
    
