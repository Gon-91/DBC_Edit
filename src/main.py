
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
    # main.py
    main()


#    print("This is the main module.")
#
#
#    datamodel = AppModel()
#    controller = FileController(datamodel)
#
#
#
#    controller.open_file("./src/controllers/sample.dbc")
#    controller.open_file("./src/controllers/sample2.dbc")
#    controller.open_file("./src/controllers/sample2.dbc")
#
#    print(datamodel.get_files_names())
