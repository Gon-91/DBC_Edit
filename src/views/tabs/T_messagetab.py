from PySide6.QtWidgets import QWidget, QVBoxLayout
from views.widgets.T_message_widget import MessageTableWidget

class MessageTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.table = MessageTableWidget
        layout.addWidget(self.table)
        