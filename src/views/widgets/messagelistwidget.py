from PySide6.QtWidgets import (
    QWidget , QDockWidget , QListWidget,QPushButton , QVBoxLayout , QTableWidget , QTableWidgetItem , QAbstractItemView,QHeaderView)
from PySide6.QtCore import Qt

class MessageListDock(QDockWidget) :
    def __init__(self, model):
        super().__init__("Message List")

        self.model = model

        self._init_ui()
        self._connect_model()
    def _init_ui(self):


        # 기본 DockWidget 옵션 설정
        # 닫기 버튼 비활성화
        self.setFeatures(
            QDockWidget.NoDockWidgetFeatures
        )


        # UI 구성
        container = QWidget(self)
        self.setWidget(container)
        main_layout = QVBoxLayout(container)


        #Table Widget에 메세지 리스트 표시
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "DLC"])

        self.table.setColumnWidth(0, 80)   # ID
        self.table.setColumnWidth(2, 60)   # DLC

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        main_layout.addWidget(self.table)






        #self.message_list_widget = QListWidget(self)
        #main_layout.addWidget(self.message_list_widget)

        #self.add_btn = QPushButton("선택 추가")
        #self.remove_btn = QPushButton("선택 제거")

        #main_layout.addWidget(self.add_btn)
        #main_layout.addWidget(self.remove_btn)

    def _connect_model(self):

        # 모델에서 파일안의 메세지 리시트 수신 및 표시
        self.model.current_file_changed.connect(self._on_messageslist)
    
        # 메세지 선택 시 
        self.table.itemClicked.connect(self._on_current_message_changed)
        #self.add_btn.clicked.connect(self._add_message)
        #self.table.itemClicked.connect(self._update_messages_list)

#    def _on_show_messageslist(self,messages):
#        self.message_list_widget.clear()
#        if messages is None :
#            return
#        for message in messages :
#            self.message_list_widget.addItem(f"{message.id} : {message.name}")

    def _on_messageslist(self,messages):
        self.table.setRowCount(0)

        if not messages:
            return

        self.table.setRowCount(3)

        for row, msg in enumerate(messages):
            self.table.setItem(row, 0, QTableWidgetItem(msg.id))
            self.table.setItem(row, 1, QTableWidgetItem(msg.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(msg.length)))
            #self.table.setItem(row, 3, QTableWidgetItem(str(len(msg.signals))))
    def _on_current_message_changed(self):
        item = self.table.selectedItems()
        
        id = item[0].text()
        name = item[0].text()
        self.model.set_current_message(id,name)
        
        

    # 메세지 추가
    def _add_message(self):
        pass
        #self.table.insertRow(self.table.rowCount())
    def _remove_message(self):
        pass
    def _modify_message(self):
        pass

    def _update_messages_list(self):
        pass
        #messages = []
        #for row in range(self.table.rowCount()):
        #    id = self.table.item(row, 0).text()
        #    name = self.table.item(row,1).text()
        #    length = int(self.table.item(row,2).text())
        #    #
        #    message = Messages(
        #        id = id,
        #        name = name,
        #        length = length,
        #        signals = []
        #    )
