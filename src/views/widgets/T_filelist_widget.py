from PySide6.QtWidgets import QListWidget

class FileListWidget(QListWidget):
    def __init__(self): 
        super().__init__()
        
    def update(self,filelist):
        self.clear()
        self.additems(filelist)

        