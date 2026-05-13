# from PyQt6 import QtWidgets, QtGui, QtCore
# from WorkWidgets.AddStuWidget import AddStuWidget
# from WorkWidgets.ShowStuWidget import ShowStuWidget
# from WorkWidgets.ModifyStuWidget import ModifyStuWidget
# from WorkWidgets.DeleteStuWidget import DeleteStuWidget
# from WorkWidgets.WidgetComponents import LabelComponent
# from WorkWidgets.WidgetComponents import ButtonComponent

# #先在main做三個widget布局
# class MainWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("main_widget")

#         layout = QtWidgets.QGridLayout()
#         header_label = LabelComponent(24, "Student Management System")
#         function_widget = FunctionWidget()
#         menu_widget = MenuWidget(function_widget.update_widget)

#         layout.addWidget(header_label, 0, 0, 1, 2)
#         layout.addWidget(menu_widget, 1, 0, 1, 1)
#         layout.addWidget(function_widget, 1, 1, 1, 1)

#         layout.setColumnStretch(0, 1)
#         layout.setColumnStretch(1, 6)
#         layout.setRowStretch(0, 1)
#         layout.setRowStretch(1, 6)

#         self.setLayout(layout)

# #
# class MenuWidget(QtWidgets.QWidget):
#     def __init__(self, update_widget_callback):
#         super().__init__()
#         self.setObjectName("menu_widget")
#         self.update_widget_callback = update_widget_callback

#         layout = QtWidgets.QVBoxLayout()
#         add_button = ButtonComponent("Add student",True)
#         show_button = ButtonComponent("Show all",True)
#         modify_button = ButtonComponent("Modify subject",True)
#         delete_button = ButtonComponent("Delete student",True)
#         # https://medium.com/seaniap/python-lambda-函式-7e86a56f1996
#         add_button.clicked.connect(lambda: self.update_widget_callback("add"))#使用 lambda 可以延遲函數的執行，確保它僅在按鈕被點擊時才執行。
#         show_button.clicked.connect(lambda: self.update_widget_callback("show"))
#         modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
#         delete_button.clicked.connect(lambda: self.update_widget_callback("delete"))

#         layout.addWidget(add_button, stretch=1)
#         layout.addWidget(show_button, stretch=1)
#         layout.addWidget(modify_button, stretch=1)
#         layout.addWidget(delete_button, stretch=1)

#         self.setLayout(layout)


# class FunctionWidget(QtWidgets.QStackedWidget):
#     def __init__(self):
#         super().__init__()
#         self.widget_dict = {
#             "add": self.addWidget(AddStuWidget()),
#             "show": self.addWidget(ShowStuWidget()),
#             "modify": self.addWidget(ModifyStuWidget()),
#             "delete": self.addWidget(DeleteStuWidget())
#         }
#         self.update_widget("add")
    
#     def update_widget(self, name):
#         self.setCurrentIndex(self.widget_dict[name])
#         current_widget = self.currentWidget()
#         current_widget.load()

#----------------
# from PyQt6 import QtWidgets, QtGui, QtCore
# from WorkWidgets.AddStuWidget import AddStuWidget
# from WorkWidgets.ShowStuWidget import ShowStuWidget
# from WorkWidgets.ModifyStuWidget import ModifyStuWidget
# from WorkWidgets.DeleteStuWidget import DeleteStuWidget
# from WorkWidgets.WidgetComponents import LabelComponent
# from WorkWidgets.WidgetComponents import ButtonComponent_p


# # 先在 main 做三個 widget 布局
# class MainWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("main_widget")

#         # 设置背景图片
#         self.set_background_image('C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/Week13_me/photo/sky.png')

#         layout = QtWidgets.QGridLayout()
#         header_label = LabelComponent(24, "Student Management System")
#         function_widget = FunctionWidget()
#         menu_widget = MenuWidget(function_widget.update_widget)

#         layout.addWidget(header_label, 0, 0, 1, 2)
#         layout.addWidget(menu_widget, 1, 0, 1, 1)
#         layout.addWidget(function_widget, 1, 1, 1, 1)

#         layout.setColumnStretch(0, 1)
#         layout.setColumnStretch(1, 6)
#         layout.setRowStretch(0, 1)
#         layout.setRowStretch(1, 6)

#         self.setLayout(layout)

#     def set_background_image(self, image_path):
#         oImage = QtGui.QImage(image_path)
#         sImage = oImage.scaled(self.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding, QtCore.Qt.TransformationMode.SmoothTransformation)
#         palette = QtGui.QPalette()
#         palette.setBrush(QtGui.QPalette.ColorRole.Window, QtGui.QBrush(sImage))
#         self.setPalette(palette)

#     def resizeEvent(self, event):
#         self.set_background_image('C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/Week13_me/photo/sky.png')
#         super().resizeEvent(event)

# class MenuWidget(QtWidgets.QWidget):
#     def __init__(self, update_widget_callback):
#         super().__init__()
#         self.setObjectName("menu_widget")
#         self.update_widget_callback = update_widget_callback

#         layout = QtWidgets.QVBoxLayout()

#         add_button = ButtonComponent_p("Add student", True, "'C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/Week13_me/photo/ocean_abstract.png'")
#         show_button =   ButtonComponent_p("Show all", True, "'C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/Week13_me/photo/ocean_abstract.png'")
#         modify_button = ButtonComponent_p("Modify subject", True, "'C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/Week13_me/photo/ocean_abstract.png'")
#         delete_button = ButtonComponent_p("Delete student", True, "'C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/Week13_me/photo/ocean_abstract.png'")
        
#         add_button.clicked.connect(lambda: self.update_widget_callback("add"))
#         show_button.clicked.connect(lambda: self.update_widget_callback("show"))
#         modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
#         delete_button.clicked.connect(lambda: self.update_widget_callback("delete"))

#         layout.addWidget(add_button, stretch=1)
#         layout.addWidget(show_button, stretch=1)
#         layout.addWidget(modify_button, stretch=1)
#         layout.addWidget(delete_button, stretch=1)

#         self.setLayout(layout)

# class FunctionWidget(QtWidgets.QStackedWidget):
#     def __init__(self):
#         super().__init__()
#         self.widget_dict = {
#             "add": self.addWidget(AddStuWidget()),
#             "show": self.addWidget(ShowStuWidget()),
#             "modify": self.addWidget(ModifyStuWidget()),
#             "delete": self.addWidget(DeleteStuWidget())
#         }
#         self.update_widget("add")
    
#     def update_widget(self, name):
#         self.setCurrentIndex(self.widget_dict[name])
#         current_widget = self.currentWidget()
#         current_widget.load()

# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     main_window = MainWidget()
#     main_window.setFixedSize(800, 600)
#     main_window.show()
#     app.exec()

from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DeleteStuWidget import DeleteStuWidget
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent_p

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")

        # Set background image
        self.set_background_image('C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/photo/sky.png')

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(menu_widget, 1, 0, 1, 1)
        layout.addWidget(function_widget, 1, 1, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)

        self.setLayout(layout)

    def set_background_image(self, image_path):
        oImage = QtGui.QImage(image_path)
        sImage = oImage.scaled(self.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding, QtCore.Qt.TransformationMode.SmoothTransformation)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.ColorRole.Window, QtGui.QBrush(sImage))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background_image('C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/photo/sky.png')
        super().resizeEvent(event)

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QVBoxLayout()

        add_button = ButtonComponent_p("Add student", True, r"C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/photo/ocean_abstract.png")
        show_button = ButtonComponent_p("Show all", True, r"C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/photo/purple_abstract.png")
        modify_button = ButtonComponent_p("Modify subject", True, r"C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/photo/orange_abstract.png")
        delete_button = ButtonComponent_p("Delete student", True, r"C:/Users/user514/Desktop/NTUTdk4t6/py_panel/widget/photo/2.png")
        
        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
        delete_button.clicked.connect(lambda: self.update_widget_callback("delete"))

        layout.addWidget(add_button, stretch=1)
        layout.addWidget(show_button, stretch=1)
        layout.addWidget(modify_button, stretch=1)
        layout.addWidget(delete_button, stretch=1)

        self.setLayout(layout)

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "add": self.addWidget(AddStuWidget()),
            "show": self.addWidget(ShowStuWidget()),
            "modify": self.addWidget(ModifyStuWidget()),
            "delete": self.addWidget(DeleteStuWidget())
        }
        self.update_widget("add")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()
