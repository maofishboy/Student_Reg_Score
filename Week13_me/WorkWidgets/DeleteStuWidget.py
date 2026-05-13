from PyQt6 import QtWidgets, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent_c
from SocketClient.ServiceController import ExecuteSendCommand
import json


class DeleteStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("del_stu_widget")
        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(20, "Delete Student")
        self.delete_widget = DeleteWidget()
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.delete_widget, stretch=9)
        self.setLayout(layout)

    def load(self):
        show_dict = {"command": "show", "parameters": {}}
        self.delete_widget.hint_label.setText("Loading student list...")
        self.send_command = ExecuteSendCommand(show_dict)
        self.send_command.return_sig.connect(self.process_show_result)
        self.send_command.start()

    def process_show_result(self, result):
        result = json.loads(result)
        if result["status"] != "OK":
            self.delete_widget.hint_label.setText("Failed to load student list.")
            self.delete_widget.populate_combo_box([])
            return

        students = result.get("parameters", {})
        student_names = [student["name"] for student in students.values()]
        self.delete_widget.populate_combo_box(student_names)


class DeleteWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("del_stu_widget")
        self.name = ""

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.combo_box_name = QtWidgets.QComboBox()
        self.combo_box_name.setMinimumHeight(30)
        self.combo_box_name.setMaximumWidth(1200)
        self.combo_box_name.currentIndexChanged.connect(self.combo_box_select_changed)

        self.hint_label = LabelComponent(16, "", "color: red;")
        self.del_button = ButtonComponent_c("Delete", enable=False)
        self.del_button.setMinimumHeight(40)
        self.del_button.setMaximumWidth(100)
        self.del_button.clicked.connect(self.del_action)

        combo_layout = QtWidgets.QHBoxLayout()
        combo_layout.addWidget(self.combo_box_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.del_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(combo_layout, stretch=1)
        layout.addWidget(self.hint_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter, stretch=1)
        layout.addLayout(button_layout, stretch=2)
        self.setLayout(layout)

    def populate_combo_box(self, student_names):
        self.combo_box_name.clear()
        self.combo_box_name.addItems(student_names)
        has_students = bool(student_names)
        self.combo_box_name.setEnabled(has_students)
        self.del_button.setEnabled(has_students)
        self.name = self.combo_box_name.currentText()
        if has_students:
            self.hint_label.setText("Select a student to delete.")
        else:
            self.hint_label.setText("No students available to delete.")

    def combo_box_select_changed(self):
        self.name = self.combo_box_name.currentText()
        self.del_button.setEnabled(bool(self.name))

    def del_action(self):
        if not self.name:
            self.hint_label.setText("Please select a student first.")
            return

        del_dict = {"command": "delete", "parameters": {"name": self.name}}
        self.hint_label.setText(f"Deleting '{self.name}'...")
        self.del_button.setEnabled(False)
        self.send_command = ExecuteSendCommand(del_dict)
        self.send_command.return_sig.connect(self.process_send_result)
        self.send_command.start()

    def process_send_result(self, result):
        result = json.loads(result)
        if result["status"] == "OK":
            deleted_name = self.name
            remaining_names = [
                self.combo_box_name.itemText(index)
                for index in range(self.combo_box_name.count())
                if self.combo_box_name.itemText(index) != deleted_name
            ]
            self.populate_combo_box(remaining_names)
            self.hint_label.setText(f"Deleted '{deleted_name}' successfully.")
        else:
            self.hint_label.setText(result.get("reason", "Delete failed."))
            self.del_button.setEnabled(bool(self.combo_box_name.currentText()))
