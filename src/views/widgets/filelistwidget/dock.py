from PySide6.QtWidgets import QWidget , QDockWidget

class FileListDock(QDockWidget) :
    def __init__(self, model):
        super().__init__("File List")
        
        self.model = model
        
        self._init_ui()
        self._connect_model()
    
    def _init_ui(self):

        self.file_list_widget = QWidget(self)
        self.setWidget(self.file_list_widget)


    def _connect_model(self):

        self.model.file_added.connect(self._on_file_added)

    
    # ---
    def _on_file_added(self, dbc_file):
        self.file_list_widget.clear()
        #for msg in dbc_file.messages:
        #    self.file_list_widget.addItem(msg.name)
        print(dbc_file)

        
