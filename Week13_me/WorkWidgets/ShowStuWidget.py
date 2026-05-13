from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent,ScrollableWidgetComponent
from SocketClient.ServiceController import ExecuteSendCommand
import time
import json


class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("show_stu_widget")
        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        self.hint_label = LabelComponent(16, "", "color: black;")
        self.scrollable_hint_label = ScrollableWidgetComponent(self.hint_label)
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.scrollable_hint_label, stretch=9)
        self.setLayout(layout)
    
    def load(self):
        show_dict = {'command': 'show', 'parameters': {}}
        self.send_command = ExecuteSendCommand(show_dict)
        self.send_command.return_sig.connect(self.process_show_result)  # 處理返回結果的槽
        self.send_command.start()

    def process_show_result(self, result):
        result = json.loads(result)
        if result['status'] == 'OK': 
            students = result['parameters']
            stu_stringlist = "\n==== student list ===="
            for student in students.values():
                stu_stringlist += f"\n\nName: {student.get('name', 'N/A')}"
                scores = student.get('scores', {})
                for subject, score in scores.items():
                    stu_stringlist += f"\n    subject: {subject}, score: {score}"
            stu_stringlist += "\n\n======================"
    
            self.hint_label.setText(stu_stringlist)
        else:
            self.hint_label.setText("Showing failed.")





