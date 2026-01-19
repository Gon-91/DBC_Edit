from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt


from views.widgets.signallist_widget import SignalTableModel,SignalListView
from views.widgets.signallayout_widget import SignalLayoutWidget

class CenteralWidget(QWidget):

    def __init__(self,vm,usecase) :
        super().__init__()

        self._viewmodel = vm
        self._uc = usecase

        self._ui()
        self._connect()

    def _ui(self):


        self.signallist_widget = SignalListView()
        self.signallayout_widget = SignalLayoutWidget()


        layout = QVBoxLayout(self)




        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.signallist_widget)
        splitter.addWidget(self.signallayout_widget)



        layout.addWidget(splitter)


    def _connect(self):
        self.signallist_widget._setmodel(self._viewmodel._signallist_table_model)
        #self._viewmodel.signals.connect(self._update_signallist)

    #def _update_signallist(self,signals):
    #    #self.signallist_widget._setmodel(SignalTableModel(signals))
    #    self._viewmodel._signallist_table_model.set_signals(signals)
    #    self.signallist_widget._setmodel(self._viewmodel._signallist_table_model)
        
        #self.signallist_widget.update_signallist(signals)