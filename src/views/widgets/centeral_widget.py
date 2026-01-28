from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt



from .signallist_widget import SignalListView
from .signallayout_widget import SignalLayoutView

# Centeral Widget ( 중앙 메인 위젯 )
class CenteralWidget(QWidget):

    def __init__(self,vm,usecase) :
        super().__init__()

        # ViewModel 과 Usecase 설정
        self._viewmodel = vm
        self._uc = usecase

        self._ui()
        self._connect()

    def _ui(self):

        # Signal List View 와 Signal Layout View 생성
        self.signallist_widget = SignalListView()
        self.signallayout_widget = SignalLayoutView(self._viewmodel._signallayoutmodel)


        layout = QVBoxLayout(self)




        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.signallist_widget)
        splitter.addWidget(self.signallayout_widget)



        layout.addWidget(splitter)


    def _connect(self):
       
        # ViewModel -> View 
        self.signallist_widget._setmodel(self._viewmodel._signallistmodel)
        self.signallayout_widget._setmodel(self._viewmodel._signallayoutmodel)
