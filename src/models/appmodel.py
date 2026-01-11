
from models.domainmodels import DBCFile
from PySide6.QtCore import QObject, Signal

"""
    Qt 기반의 최상위 모델
"""

class AppModel(QObject):

    #file_added = Signal(DBCFile)
    file_added = Signal(list[str])
    current_file_changed = Signal(DBCFile | None )

    def __init__(self):
        super().__init__()
        self._dbc_files : list[DBCFile] = []
        self._current_dbc_file : DBCFile | None = None

    def add_file(self, dbc_file : DBCFile):
        if dbc_file.file_path in [f.file_path for f in self._dbc_files]:
            return
        self._dbc_files.append(dbc_file)
        #self.file_added.emit(dbc_file)
        self.file_added.emit(self.get_files_names())
        self._current_dbc_file = dbc_file

    def remove_file(self, dbc_file : DBCFile):
        if dbc_file in self._dbc_files:
            self._dbc_files.remove(dbc_file)
            self._current_dbc_file = self._dbc_files[-1] if self._dbc_files else None

    def get_files(self) -> list[DBCFile]:
        return self._dbc_files
    def get_files_count(self) -> int :
        return len(self._dbc_files)
    def get_files_names(self) -> list[str]:
        return [file.file_name for file in self._dbc_files]

    def get_current_file(self) -> DBCFile | None : 
        return self._current_dbc_file

    def set_current_file(self, dbc_file : DBCFile | None ):
        self._current_dbc_file = dbc_file
        self.current_file_changed.emit(dbc_file)
