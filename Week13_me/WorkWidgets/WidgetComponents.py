from PyQt6 import QtWidgets, QtGui, QtCore


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, text, text_color="color: black;"):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=100))
        self.setText(text)
        self.setStyleSheet(text_color)


class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, text="", enable=False, length=10, width=400, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(text)
        self.setEnabled(enable)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("Arial", font_size))


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, enable=False, font_size=16):
        super().__init__()
        self.setText(text)
        self.setEnabled(enable)
        self.setFont(QtGui.QFont("Arial", font_size))


class ButtonComponent_c(QtWidgets.QPushButton):
    def __init__(self, text, enable=False, font_size=16, background_color="brown", text_color="white"):
        super().__init__()
        self.setText(text)
        self.setEnabled(enable)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.set_colors(background_color, text_color)

    def set_colors(self, background_color, text_color):
        style = ""
        if background_color:
            style += f"background-color: {background_color};"
        if text_color:
            style += f"color: {text_color};"
        self.setStyleSheet(style)


class ScrollableWidgetComponent(QtWidgets.QWidget):
    def __init__(self, label_content):
        super().__init__()
        self.scrollplace = QtWidgets.QScrollArea()
        self.scrollplace.setWidget(label_content)
        self.scrollplace.setWidgetResizable(True)
        self.scrollplace.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.scrollplace)
        self.setLayout(self.layout)
