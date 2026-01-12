from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt


from views.widgets.signallistwidget import SignalListDock
#from views.widgets.messagelayoutwidget import MessageLayoutDock

class MainWidget(QWidget):

    def __init__(self, model) :
        super().__init__()

        self.model = model

        self._init_ui()
        self._connect_model()

    def _init_ui(self):


        layout = QVBoxLayout(self)


        self.SignalListDock = SignalListDock(self.model)


        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.SignalListDock)



        layout.addWidget(splitter)


        #splitter.addWidget(detail_view)
    def _connect_model(self):
        pass