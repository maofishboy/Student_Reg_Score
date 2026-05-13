from PyQt6 import QtWidgets
from WorkWidgets.WidgetComponents import LabelComponent, ScrollableWidgetComponent
from SocketClient.ServiceController import ExecuteSendCommand
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
        show_dict = {"command": "show", "parameters": {}}
        self.hint_label.setText("Loading student data...")
        self.send_command = ExecuteSendCommand(show_dict)
        self.send_command.return_sig.connect(self.process_show_result)
        self.send_command.start()

    def process_show_result(self, result):
        result = json.loads(result)
        if result["status"] != "OK":
            self.hint_label.setText("Showing failed.")
            return

        students = result.get("parameters", {})
        if not students:
            self.hint_label.setText("No student data yet.")
            return

        lines = ["==== student list ===="]
        for student in students.values():
            lines.append("")
            lines.append(f"Name: {student.get('name', 'N/A')}")
            scores = student.get("scores", {})
            if not scores:
                lines.append("    No subjects yet.")
            else:
                for subject, score in scores.items():
                    lines.append(f"    Subject: {subject}, Score: {score}")
        lines.append("")
        lines.append("======================")
        self.hint_label.setText("\n".join(lines))
