from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QObject, Signal
class FileListWidget(QListWidget):

    selectedfile = Signal(str)

    def __init__(self): 
        super().__init__()
        
        self.currentItemChanged.connect(self._currentitem)




    def update_filelist(self,filelist):
        self.clear()
        self.addItems(filelist)

    def remove_file(self):
        self.removeItemWidget(self.currentIndex())
    
    def _currentitem(self):
        self.selectedfile.emit(self.currentItem().text())
        #print(self.currentItem().text())
        #return self.currentItem().text()
