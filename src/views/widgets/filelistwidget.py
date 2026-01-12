from PySide6.QtWidgets import QWidget , QDockWidget , QListWidget, QVBoxLayout
from PySide6.QtCore import Qt
class FileListDock(QDockWidget) :
    def __init__(self, model):
        super().__init__("File List")
        
        self.model = model
        
        self._init_ui()
        self._connect_model()
    
    def _init_ui(self):

        self.setFeatures(
            QDockWidget.NoDockWidgetFeatures
        )


        container = QWidget(self)
        self.setWidget(container)

        main_layout = QVBoxLayout(container)
        self.file_list_widget = QListWidget(self)

        main_layout.addWidget(self.file_list_widget)


        #self.file_list_widget = QListWidget(self)
        #self.setWidget(self.file_list_widget)


    def _connect_model(self):

        self.file_list_widget.currentItemChanged.connect(
            self._on_current_file_changed
        )



        self.model.files_changed.connect(self._on_file_list_changed)
        #self.model.files_changed.connect(self._on_file_list_changed)

    
    # ---
    def _on_file_list_changed(self,dbc_files : list[str]):
        self.file_list_widget.clear()
        for dbc_file in dbc_files:
            self.file_list_widget.addItem(dbc_file)

    def _on_current_file_changed(self, selected_item):
        if selected_item is None : 
            return
        self.model.set_current_file(selected_item.text())

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Delete:
            self.model.remove_file(self.file_list_widget.currentItem().text())
