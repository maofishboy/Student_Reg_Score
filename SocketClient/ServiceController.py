from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from SocketClient.SocketClient import SocketClient
import json

class ExecuteSendCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, data):
        super().__init__()
        self.data = data  # 接收字典格式的數據

    def run(self):
        client = None
        try:
            client = SocketClient()
            client.send_command(self.data['command'], self.data['parameters'])
            response = client.wait_response()
        except Exception as error:
            response = {"status": "Fail", "reason": f"Connection error: {error}"}
        finally:
            if client is not None:
                client.close()

        self.return_sig.emit(json.dumps(response))
    
