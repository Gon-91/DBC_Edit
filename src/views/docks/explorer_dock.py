
from PySide6.QtWidgets import QDockWidget, QTabWidget
from PySide6.QtCore import Qt

from views.tabs.filetab import FileTab
from views.tabs.messagetab import MessageTab


class ExplorerDock(QDockWidget):
    def __init__(self,vm,usecase):
        super().__init__("Explorer")

        self.setFeatures(
            QDockWidget.NoDockWidgetFeatures
        )

        self._viewmodel = vm
        self._uc = usecase

        self._ui()
        self._connect()


    def _ui(self):

        self.filetab = FileTab()
        self.messagetab = MessageTab()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        tabs.addTab(self.filetab, "Files")
        tabs.addTab(self.messagetab, "Messages")

        self.setWidget(tabs)

        self.setMinimumSize(200, 200)

    def _connect(self):

        self.filetab.filelistwidget.selectedfile.connect(self._on_file_selected)
        self.messagetab.table.selectedmessage.connect(self._on_message_selected)



        self._viewmodel.files.connect(self._update_filelist)
        self._viewmodel.messages.connect(self._update_messagelist)

    # === On 메서드 ===
    # === 사용자 입력 --> 유스케이스

    def _on_file_selected(self,filename):
        self._uc.get("file.select").execute(filename)

    def _on_message_selected(self,messageviewdata):
        self._uc.get("message.select").execute(messageviewdata)


    # === 뷰모델로부터 --> 뷰 동작
    def _update_filelist(self,filelist):
        self.filetab.update_filelist(filelist)


    # === 뷰모델로부터 가공된 메세지리스트 전달 
    # messages = [message]
    # message = { "id" : id , "name" : name , "length" : length }
    def _update_messagelist(self,messagelist):
        self.messagetab.update_messagelist(messagelist)


    # === Key event
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            file_name = self.filetab.filelistwidget.currentItem().text()
            self._uc.get("file.close").execute(file_name)

            #log
            print("View : KeyPressEvent")
