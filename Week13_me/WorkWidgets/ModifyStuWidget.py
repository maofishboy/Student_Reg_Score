from PyQt6 import QtWidgets, QtGui
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ButtonComponent_c
from SocketClient.ServiceController import ExecuteSendCommand
import json

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("mod_sub_widget")
        layout = QtWidgets.QVBoxLayout()
        header_label = LabelComponent(20, "Modify Subject")
        self.radio_button_change = QtWidgets.QRadioButton('Change')
        self.radio_button_add = QtWidgets.QRadioButton('Add new')
        self.radio_button_change.toggled.connect(self.radio_button_change_on_clicked)
        self.radio_button_add.toggled.connect(self.radio_button_add_on_clicked)
        self.mod_widget = ChangeWidget(parent=self)  
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.radio_button_change, stretch=1)
        layout.addWidget(self.radio_button_add, stretch=1)
        layout.addWidget(self.mod_widget, stretch=7)
        self.setLayout(layout)
    
    def radio_button_change_on_clicked(self):
        if self.radio_button_change.isChecked():
            self.mod_widget.deleteLater()
            self.mod_widget = ChangeWidget(parent=self)  # 确保传递parent参数
            self.layout().addWidget(self.mod_widget, stretch=7)
            self.populate_change_widgets()

    def radio_button_add_on_clicked(self):
        if self.radio_button_add.isChecked():
            self.mod_widget.deleteLater()
            self.mod_widget = AddNewWidget(parent=self)
            self.layout().addWidget(self.mod_widget, stretch=7)
            self.populate_add_widgets()

    def populate_change_widgets(self):
        if hasattr(self, 'result'):
            student_names = [student['name'] for student in self.result['parameters'].values()]
            self.mod_widget.populate_combo_box_name(student_names)
            now_name = self.mod_widget.name if hasattr(self.mod_widget, 'name') else None
            if now_name and now_name in self.result['parameters']:
                all_subjects = list(self.result['parameters'][now_name]['scores'].keys())
                if isinstance(self.mod_widget, ChangeWidget):
                    self.mod_widget.populate_combo_box_sub(all_subjects)

    def populate_add_widgets(self):
        if hasattr(self, 'result'):
            student_names = [student['name'] for student in self.result['parameters'].values()]
            self.mod_widget.populate_combo_box_name(student_names)
            self.mod_widget.subject_editor_label.clear()
            self.mod_widget.combo_box_score.setEnabled(False)
            self.mod_widget.add_new_button.setEnabled(False)

    def load(self):
        show_dict = {'command': 'show', 'parameters': {}}
        self.send_command = ExecuteSendCommand(show_dict)
        self.send_command.return_sig.connect(self.process_show_result)
        self.send_command.start()
    
    def process_show_result(self, result):
        self.result = json.loads(result)
        if self.result['status'] == 'OK':
            self.populate_change_widgets()  # 默认填充 ChangeWidget


class ChangeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("change_sub_widget")
        layout = QtWidgets.QVBoxLayout()
        self.combo_box_name = QtWidgets.QComboBox()
        self.combo_box_name.currentIndexChanged.connect(self.combo_box_name_select_changed)
        self.combo_box_sub = QtWidgets.QComboBox()
        self.combo_box_sub.currentIndexChanged.connect(self.combo_box_sub_select_changed)
        self.combo_box_score = QtWidgets.QComboBox()
        self.combo_box_score.currentIndexChanged.connect(self.combo_box_score_select_changed)
        self.combo_box_score.addItems([str(i) for i in range(101)])
        self.change_button = ButtonComponent_c("Change", enable=True)
        self.change_button.clicked.connect(self.change_action)

        layout.addWidget(self.combo_box_name)
        layout.addWidget(self.combo_box_sub)
        layout.addWidget(self.combo_box_score)
        layout.addWidget(self.change_button)
        
        self.setLayout(layout)

    def populate_combo_box_name(self, student_names):
        self.combo_box_name.clear()
        self.combo_box_name.addItems(student_names)

    def populate_combo_box_sub(self, subjects):
        self.combo_box_sub.clear()
        self.combo_box_sub.addItems(subjects)
    
    def combo_box_name_select_changed(self):
        self.name = self.combo_box_name.currentText()
        parent_widget = self.parentWidget()
        if parent_widget:
            students = parent_widget.result['parameters']
            if self.name in students:
                subjects = list(students[self.name]['scores'].keys())
                self.populate_combo_box_sub(subjects)

    def combo_box_sub_select_changed(self):
        self.subject = self.combo_box_sub.currentText()

    def combo_box_score_select_changed(self):
        self.score = self.combo_box_score.currentText()
        

    def change_action(self):
        parent_widget = self.parentWidget()
        if parent_widget:
            student_dict = parent_widget.result['parameters']
            student_dict[self.name]['scores'][self.subject] = self.score
            change_dict = {'command': 'modify', 'parameters': student_dict[self.name]}
            self.send_command = ExecuteSendCommand(change_dict)
            self.send_command.return_sig.connect(self.process_send_result)
            self.send_command.start() 

    def process_send_result(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            self.change_button.setEnabled(False)
        else:
            self.change_button.setEnabled(True)


class AddNewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("add_newsub_widget")
        layout = QtWidgets.QVBoxLayout()
        self.combo_box_name = QtWidgets.QComboBox()
        self.combo_box_name.currentIndexChanged.connect(self.combo_box_name_select_changed)
        self.subject_label = LabelComponent(14, "Subject:")
        self.subject_editor_label = LineEditComponent("", enable=True)  # 将 enable 设置为 True
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
        self.combo_box_name.addItems(student_names)
    
    def combo_box_name_select_changed(self):
        self.name = self.combo_box_name.currentText()
        parent_widget = self.parentWidget()
        if parent_widget:
            students = parent_widget.result['parameters']
            if self.name in students:
                self.subjects = list(students[self.name]['scores'].keys())

    def subject_change(self):
        self.new_subject = self.subject_editor_label.text()
        if self.new_subject in self.subjects:
            self.combo_box_score.setEnabled(False)
            self.add_new_button.setEnabled(False)
        else:
            self.combo_box_score.setEnabled(True)
            self.add_new_button.setEnabled(True)

    def combo_box_score_select_changed(self):
        self.score = self.combo_box_score.currentText()
        
    
    def add_new_action(self):
        parent_widget = self.parentWidget()
        if parent_widget:
            student_dict = parent_widget.result['parameters']
            student_dict[self.name]['scores'][self.new_subject] = self.score
            add_new_dict = {'command': 'modify', 'parameters': student_dict[self.name]}
            self.send_command = ExecuteSendCommand(add_new_dict)
            self.send_command.return_sig.connect(self.process_send_result)
            self.send_command.start()

    def process_send_result(self, result):
        result = json.loads(result)
        if result['status'] == 'OK':
            self.add_new_button.setEnabled(False)
            self.subject_editor_label.clear()
            self.combo_box_score.setEnabled(False)
        else:
            self.add_new_button.setEnabled(True)









