
# main.py
import sys
from PySide6.QtWidgets import QApplication
from app.app_initializer import create_main_window


def main():
    app = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    sys.exit(app.exec())


if __name__=="__main__":
    main()

