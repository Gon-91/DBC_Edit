from PySide6.QtWidgets import QTableWidget ,  QAbstractItemView, QHeaderView,QTableWidgetItem
from PySide6.QtGui import QColor


class SignalLayoutWidget(QTableWidget):

    def __init__(self):
        super().__init__()