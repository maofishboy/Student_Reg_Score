from PyQt6 import QtWidgets
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent_c
from SocketClient.ServiceController import ExecuteSendCommand
import json


class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("mod_sub_widget")
        self.result = {"parameters": {}}

        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(20, "Modify Subject")
        self.hint_label = LabelComponent(14, "", "color: red;")
        self.radio_button_change = QtWidgets.QRadioButton("Change")
        self.radio_button_add = QtWidgets.QRadioButton("Add new")
        self.radio_button_change.toggled.connect(self.radio_button_change_on_clicked)
        self.radio_button_add.toggled.connect(self.radio_button_add_on_clicked)
        self.mod_widget = ChangeWidget(parent=self)

        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.hint_label, stretch=1)
        layout.addWidget(self.radio_button_change, stretch=1)
        layout.addWidget(self.radio_button_add, stretch=1)
        layout.addWidget(self.mod_widget, stretch=7)
        self.setLayout(layout)

        self.radio_button_change.setChecked(True)

    def set_hint(self, text):
        self.hint_label.setText(text)

    def radio_button_change_on_clicked(self):
        if self.radio_button_change.isChecked():
            self.mod_widget.deleteLater()
            self.mod_widget = ChangeWidget(parent=self)
            self.layout().addWidget(self.mod_widget, stretch=7)
            self.populate_change_widgets()

    def radio_button_add_on_clicked(self):
        if self.radio_button_add.isChecked():
            self.mod_widget.deleteLater()
            self.mod_widget = AddNewWidget(parent=self)
            self.layout().addWidget(self.mod_widget, stretch=7)
            self.populate_add_widgets()

    def populate_change_widgets(self):
        students = self.result.get("parameters", {})
        student_names = [student["name"] for student in students.values()]
        self.mod_widget.populate_combo_box_name(student_names)
        if student_names:
            self.set_hint("Select a student, subject, and new score.")
        else:
            self.set_hint("No students available to modify.")

    def populate_add_widgets(self):
        students = self.result.get("parameters", {})
        student_names = [student["name"] for student in students.values()]
        self.mod_widget.populate_combo_box_name(student_names)
        if student_names:
            self.set_hint("Select a student and add a new subject.")
        else:
            self.set_hint("No students available to modify.")

    def load(self):
        show_dict = {"command": "show", "parameters": {}}
        self.set_hint("Loading student data...")
        self.send_command = ExecuteSendCommand(show_dict)
        self.send_command.return_sig.connect(self.process_show_result)
        self.send_command.start()

    def process_show_result(self, result):
        self.result = json.loads(result)
        if self.result["status"] != "OK":
            self.set_hint("Failed to load student data.")
            return

        if self.radio_button_add.isChecked():
            self.populate_add_widgets()
        else:
            self.populate_change_widgets()


class ChangeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("change_sub_widget")
        self.name = ""
        self.subject = ""
        self.score = "0"

        layout = QtWidgets.QVBoxLayout()
        self.combo_box_name = QtWidgets.QComboBox()
        self.combo_box_name.currentIndexChanged.connect(self.combo_box_name_select_changed)
        self.combo_box_sub = QtWidgets.QComboBox()
        self.combo_box_sub.currentIndexChanged.connect(self.combo_box_sub_select_changed)
        self.combo_box_score = QtWidgets.QComboBox()
        self.combo_box_score.currentIndexChanged.connect(self.combo_box_score_select_changed)
        self.combo_box_score.addItems([str(i) for i in range(101)])
        self.change_button = ButtonComponent_c("Change", enable=False)
        self.change_button.clicked.connect(self.change_action)

        layout.addWidget(self.combo_box_name)
        layout.addWidget(self.combo_box_sub)
        layout.addWidget(self.combo_box_score)
        layout.addWidget(self.change_button)
        self.setLayout(layout)

    def populate_combo_box_name(self, student_names):
        self.combo_box_name.clear()
        self.combo_box_sub.clear()
        self.change_button.setEnabled(bool(student_names))
        if student_names:
            self.combo_box_name.addItems(student_names)
            self.combo_box_name_select_changed()

    def populate_combo_box_sub(self, subjects):
        self.combo_box_sub.clear()
        self.change_button.setEnabled(bool(subjects))
        if subjects:
            self.combo_box_sub.addItems(subjects)
            self.combo_box_sub_select_changed()

    def combo_box_name_select_changed(self):
        self.name = self.combo_box_name.currentText()
        parent_widget = self.parentWidget()
        if parent_widget:
            students = parent_widget.result["parameters"]
            if self.name in students:
                subjects = list(students[self.name]["scores"].keys())
                self.populate_combo_box_sub(subjects)

    def combo_box_sub_select_changed(self):
        self.subject = self.combo_box_sub.currentText()

    def combo_box_score_select_changed(self):
        self.score = self.combo_box_score.currentText()

    def change_action(self):
        parent_widget = self.parentWidget()
        if not parent_widget or not self.name or not self.subject:
            return

        student_dict = parent_widget.result["parameters"]
        student_dict[self.name]["scores"][self.subject] = int(self.score)
        change_dict = {"command": "modify", "parameters": student_dict[self.name]}
        parent_widget.set_hint(f"Updating {self.name}'s {self.subject} score...")
        self.send_command = ExecuteSendCommand(change_dict)
        self.send_command.return_sig.connect(self.process_send_result)
        self.send_command.start()

    def process_send_result(self, result):
        parent_widget = self.parentWidget()
        result = json.loads(result)
        if result["status"] == "OK":
            parent_widget.set_hint(f"Updated {self.name}'s {self.subject} score to {self.score}.")
        else:
            parent_widget.set_hint(result.get("reason", "Change failed."))


class AddNewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("add_newsub_widget")
        self.name = ""
        self.new_subject = ""
        self.score = "0"
        self.subjects = []

        layout = QtWidgets.QVBoxLayout()
        self.combo_box_name = QtWidgets.QComboBox()
        self.combo_box_name.currentIndexChanged.connect(self.combo_box_name_select_changed)
        self.subject_label = LabelComponent(14, "Subject:")
        self.subject_editor_label = LineEditComponent("", enable=True)
        self.subject_editor_label.textChanged.connect(self.subject_change)
        self.combo_box_score = QtWidgets.QComboBox()
        self.combo_box_score.setEnabled(False)
        self.combo_box_score.currentIndexChanged.connect(self.combo_box_score_select_changed)
        self.combo_box_score.addItems([str(i) for i in range(101)])
        self.add_new_button = ButtonComponent_c("Add New", enable=False)
        self.add_new_button.clicked.connect(self.add_new_action)

        layout.addWidget(self.combo_box_name)
        layout.addStretch(1)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_editor_label)
        layout.addStretch(1)
        layout.addWidget(self.combo_box_score)
        layout.addStretch(1)
        layout.addWidget(self.add_new_button)
        self.setLayout(layout)

    def populate_combo_box_name(self, student_names):
        self.combo_box_name.clear()
        self.subject_editor_label.clear()
        self.combo_box_score.setEnabled(False)
        self.add_new_button.setEnabled(False)
        if student_names:
            self.combo_box_name.addItems(student_names)
            self.combo_box_name_select_changed()

    def combo_box_name_select_changed(self):
        self.name = self.combo_box_name.currentText()
        parent_widget = self.parentWidget()
        if parent_widget:
            students = parent_widget.result["parameters"]
            if self.name in students:
                self.subjects = list(students[self.name]["scores"].keys())

    def subject_change(self):
        self.new_subject = self.subject_editor_label.text().strip()
        already_exists = self.new_subject in self.subjects
        can_add = bool(self.new_subject) and not already_exists
        self.combo_box_score.setEnabled(can_add)
        self.add_new_button.setEnabled(can_add)
        parent_widget = self.parentWidget()
        if parent_widget and already_exists:
            parent_widget.set_hint("This subject already exists for the selected student.")

    def combo_box_score_select_changed(self):
        self.score = self.combo_box_score.currentText()

    def add_new_action(self):
        parent_widget = self.parentWidget()
        if not parent_widget or not self.name or not self.new_subject:
            return

        student_dict = parent_widget.result["parameters"]
        student_dict[self.name]["scores"][self.new_subject] = int(self.score)
        add_new_dict = {"command": "modify", "parameters": student_dict[self.name]}
        parent_widget.set_hint(f"Adding new subject '{self.new_subject}' for {self.name}...")
        self.send_command = ExecuteSendCommand(add_new_dict)
        self.send_command.return_sig.connect(self.process_send_result)
        self.send_command.start()

    def process_send_result(self, result):
        parent_widget = self.parentWidget()
        result = json.loads(result)
        if result["status"] == "OK":
            self.subjects.append(self.new_subject)
            self.subject_editor_label.clear()
            self.combo_box_score.setEnabled(False)
            self.add_new_button.setEnabled(False)
            parent_widget.set_hint(f"Added new subject '{self.new_subject}' for {self.name}.")
        else:
            parent_widget.set_hint(result.get("reason", "Add new subject failed."))
