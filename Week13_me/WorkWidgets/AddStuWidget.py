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
        self.subject_editor_label.textChanged.connect(self.subject_change)
        self.score_editor_label = LineEditComponent("")
        self.score_editor_label.textChanged.connect(self.score_change)
        self.score_editor_label.mousePressEvent = self.score_click
        self.score_editor_label.setValidator(QtGui.QIntValidator(0, 100))
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
        self.student_scores = {}
        self.reset_form()

    def reset_form(self, hint_text=""):
        self.student_scores.clear()
        self.name_editor_label.setText("Name")
        self.subject_editor_label.setText("Subject")
        self.score_editor_label.clear()
        self.hint_label.setText(hint_text)
        self.name_editor_label.setEnabled(True)
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.query_button.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)

    def load(self):
        self.reset_form()

    def name_click(self, event):
        self.name_editor_label.clear()
        self.subject_editor_label.clear()
        self.score_editor_label.clear()
        self.hint_label.clear()
        self.subject_editor_label.setEnabled(False)
        self.score_editor_label.setEnabled(False)
        self.add_button.setEnabled(False)
        self.send_button.setEnabled(False)

    def name_change(self):
        has_name = bool(self.name_editor_label.text().strip()) and self.name_editor_label.text() != "Name"
        self.query_button.setEnabled(has_name)

    def subject_click(self, event):
        self.subject_editor_label.clear()
        self.score_editor_label.clear()
        self.add_button.setEnabled(False)

    def subject_change(self):
        self.score_change()

    def score_click(self, event):
        self.score_editor_label.clear()

    def score_change(self):
        has_subject = bool(self.subject_editor_label.text().strip()) and self.subject_editor_label.text() != "Subject"
        has_score = bool(self.score_editor_label.text().strip())
        self.add_button.setEnabled(has_subject and has_score)

    def query_action(self):
        name = self.name_editor_label.text().strip()
        if not name or name == "Name":
            self.hint_label.setText("Please enter a student name first.")
            return

        query_dict = {"command": "query", "parameters": {"name": name}}
        self.hint_label.setText(f"Checking whether '{name}' already exists...")
        self.query_button.setEnabled(False)
        self.send_command = ExecuteSendCommand(query_dict)
        self.send_command.return_sig.connect(self.process_query_result)
        self.send_command.start()

    def add_action(self):
        name = self.name_editor_label.text().strip()
        subject = self.subject_editor_label.text().strip()
        score_text = self.score_editor_label.text().strip()

        if not subject or subject == "Subject" or not score_text:
            self.hint_label.setText("Please enter both subject and score.")
            return

        if name not in self.student_scores:
            self.student_scores[name] = {}

        self.student_scores[name][subject] = int(score_text)
        self.hint_label.setText(f"Added {subject}: {score_text}. You can add more subjects or press Send.")
        self.name_editor_label.setEnabled(False)
        self.subject_editor_label.clear()
        self.score_editor_label.clear()
        self.subject_editor_label.setFocus()
        self.send_button.setEnabled(True)
        self.add_button.setEnabled(False)

    def send_action(self):
        name = self.name_editor_label.text().strip()
        scores = self.student_scores.get(name, {})
        if not scores:
            self.hint_label.setText("Please add at least one subject before sending.")
            return

        send_dict = {"command": "add", "parameters": {"name": name, "scores": scores}}
        self.hint_label.setText(f"Sending data for '{name}'...")
        self.send_button.setEnabled(False)
        self.send_command = ExecuteSendCommand(send_dict)
        self.send_command.return_sig.connect(self.process_send_result)
        self.send_command.start()

    def process_query_result(self, result):
        result = json.loads(result)
        if result["status"] == "OK":
            scores = result.get("scores", {})
            score_text = ", ".join([f"{subject}: {score}" for subject, score in scores.items()]) or "no scores"
            self.hint_label.setText(f"Student already exists. Current scores: {score_text}. Use Modify to change data.")
            self.subject_editor_label.setEnabled(False)
            self.score_editor_label.setEnabled(False)
            self.add_button.setEnabled(False)
            self.send_button.setEnabled(False)
            self.name_editor_label.setEnabled(True)
        else:
            self.hint_label.setText(f"'{self.name_editor_label.text().strip()}' is a new student. Enter subjects below.")
            self.subject_editor_label.clear()
            self.score_editor_label.clear()
            self.subject_editor_label.setEnabled(True)
            self.score_editor_label.setEnabled(True)
            self.subject_editor_label.setFocus()

    def process_send_result(self, result):
        result = json.loads(result)
        if result["status"] == "OK":
            name = self.name_editor_label.text().strip()
            self.reset_form(f"Student '{name}' was added successfully.")
        else:
            self.hint_label.setText(result.get("reason", "Sending failed."))
            self.send_button.setEnabled(True)
