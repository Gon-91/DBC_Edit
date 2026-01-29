"""
filelist_widget.py
View 계층: 파일 리스트 위젯
"""
from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QObject, Signal

class FileListWidget(QListWidget):
    """
    파일 리스트를 표시하는 QListWidget 기반 위젯. 파일 선택 시 selectedfile 시그널 emit.
    """
    selectedfile = Signal(str)

    def __init__(self):
        super().__init__()
        self.currentItemChanged.connect(self._currentitem)

    def update_filelist(self, filelist: list[str]) -> None:
        """
        파일 리스트를 갱신합니다.
        Args:
            filelist (list[str]): 파일명 리스트
        """
        self.clear()
        self.addItems(filelist)

    def remove_file(self) -> None:
        """
        현재 선택된 파일을 리스트에서 제거합니다.
        """
        self.removeItemWidget(self.currentIndex())

    def _currentitem(self) -> None:
        """
        선택된 파일이 변경될 때 selectedfile 시그널 emit
        """
        self.selectedfile.emit(self.currentItem().text())
