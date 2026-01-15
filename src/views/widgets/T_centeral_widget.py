from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt


from views.widgets.T_signallist_widget import SignalListWidget
from views.widgets.T_signallayout_widget import SignalLayoutWidget

class CenteralWidget(QWidget):

    def __init__(self,vm,usecase) :
        super().__init__()

        self._viewmodel = vm
        self._uc = usecase

        self._ui()
        self._connect()

    def _ui(self):



        self.signallist_widget = SignalListWidget()
        self.signallayout_widget = SignalLayoutWidget()


        layout = QVBoxLayout(self)




        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.signallist_widget)
        splitter.addWidget(self.signallayout_widget)



        layout.addWidget(splitter)


    def _connect(self):

        self._viewmodel.signals.connect(self._update_signallist)

    def _update_signallist(self,signals):
        self.signallist_widget.update_signallist(signals)