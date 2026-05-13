from PyQt6 import QtWidgets, QtGui
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ButtonComponent_c
from SocketClient.ServiceController import ExecuteSendCommand
import json

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        self.name_label = LabelComponent(16, "Name:")
        self.subject_label = LabelComponent(16, "Subject:")
        self.score_label = LabelComponent(16, "Score:")
        self.hint_label = LabelComponent(16, "", "color: red;")
        self.name_editor_label = LineEditComponent("Name", True)
        self.name_editor_label.mousePressEvent = self.name_click
        self.name_editor_label.textChanged.connect(self.name_change)
        self.subject_editor_label = LineEditComponent("")
        self.subject_editor_label.mousePressEvent = self.subject_click
        self.score_editor_label = LineEditComponent("")
        self.score_editor_label.textChanged.connect(self.score_change)
        self.score_editor_label.mousePressEvent = self.score_click
        self.score_editor_label.setValidator(QtGui.QIntValidator(0, 999))  # 設置只允許輸入 0 到 999 的整數
        self.query_button = ButtonComponent("Query")
        self.query_button.clicked.connect(self.query_action)
        self.add_button = ButtonComponent("Add")
        self.add_button.clicked.connect(self.add_action)
        self.send_button = ButtonComponent_c("Send")
        self.send_button.clicked.connect(self.send_action)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.hint_label, 0, 3, 3, 1)
        layout.addWidget(self.name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_editor_label, 1, 1, 1, 1)
        layout.addWidget(self.query_button, 1, 2, 1, 1)
        layout.addWidget(self.subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_editor_label, 2, 1, 1, 1)
        layout.addWidget(self.score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 1) 
        layout.addWidget(self.add_button, 3, 2, 1, 1)
        layout.addWidget(self.send_button, 6, 3, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 4)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 1)
        layout.setRowStretch(6, 1)

        self.setLayout(layout)

        self.student_scores = dict()

    def load(self):
        self.name_editor_label.setText("Name")
        self.subject_editor_label.setText("Subject")
        self.score_editor_label.setText("")
        self.query_button.setEnabled(False)  
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)
        self.name_editor_label.setEnabled(True)

    def name_click(self, event):
        self.name_editor_label.clear()
        self.subject_editor_label.clear()
        self.score_editor_label.clear()
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)

    def name_change(self):
        if self.name_editor_label.text().strip():
            self.query_button.setEnabled(True)
        else:
            self.query_button.setEnabled(False)

    def subject_click(self, event):
        self.subject_editor_label.clear()
        self.score_editor_label.clear()
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)

    def score_click(self, event):
        self.score_editor_label.clear()
    
    def score_change(self):
        if self.subject_editor_label.text().strip() and self.score_editor_label.text():
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)


    def add_action(self):
        if self.name_editor_label.text() not in self.student_scores:
            self.student_scores[self.name_editor_label.text()] = {}
        self.student_scores[self.name_editor_label.text()][self.subject_editor_label.text()] = self.score_editor_label.text()
        self.hint_label.setText(f"Student {self.name_editor_label.text()}'s subject '{self.subject_editor_label.text()}' with score '{self.score_editor_label.text()}' added")
        print(f"{{'name': '{self.name_editor_label.text()}', 'scores': {{'{self.subject_editor_label.text()}': '{self.score_editor_label.text()}'}}}}")
        self.send_button.setEnabled(True)
        self.name_editor_label.setEnabled(False)
        self.add_button.setEnabled(False)



    def query_action(self):
        # 構建查詢的字典
        query_dict = {'command': 'query', 'parameters': {'name': self.name_editor_label.text()}}
        self.send_command = ExecuteSendCommand(query_dict)
        self.send_command.return_sig.connect(self.process_query_result)  # 處理返回結果的槽
        self.send_command.start()

    def send_action(self):
        # 構建發送的字典
        scores = self.student_scores.get(self.name_editor_label.text(), {})
        send_dict = {'command': 'add', 'parameters': {'name': self.name_editor_label.text(), 'scores': scores}}
        self.send_command = ExecuteSendCommand(send_dict)
        self.send_command.return_sig.connect(self.process_send_result)  # 處理返回結果的槽
        self.send_command.start()

    def process_query_result(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            pass
        else:
            self.hint_label.setText("Please enter subjects for student '{0}'".format(self.name_editor_label.text()))
            self.subject_editor_label.setText("Subject")
            self.query_button.setEnabled(False)
            self.subject_editor_label.setEnabled(True)
            self.score_editor_label.setEnabled(True)
            self.subject_editor_label.setFocus()
            self.subject_editor_label.selectAll() 

    def process_send_result(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            scores = self.student_scores.get(self.name_editor_label.text(), {})
            self.hint_label.setText(f"The infomation {{'name': '{self.name_editor_label.text()}', 'scores': {scores}}}  is sent.") 
            self.name_editor_label.setText("Name")
            self.subject_editor_label.setText("Subject")
            self.score_editor_label.setText("")
            self.query_button.setEnabled(False)  
            self.subject_editor_label.setEnabled(False)
            self.score_editor_label.setEnabled(False)
            self.add_button.setEnabled(False)
            self.send_button.setEnabled(False)
            self.name_editor_label.setEnabled(True)
            self.student_scores.clear()
        else:
            self.hint_label.setText("Sending failed.")