import sys
from PyQt6.QtWidgets import QApplication
from WorkWidgets.MainWidget import MainWidget


def main():
    app = QApplication([])
    main_window = MainWidget()
    main_window.setFixedSize(900, 600)
    main_window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
