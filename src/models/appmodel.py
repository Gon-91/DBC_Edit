
from models.domainmodels import DBCFile
from PySide6.QtCore import QObject, Signal



class AppModel(QObject):

    #file_added = Signal(DBCFile)
    #file_added = Signal(object) # list[str]
    #file_removed = Signal(object)
    files_changed = Signal(list)
    current_file_changed = Signal(object)
    current_message_changed = Signal(object)

    def __init__(self):
        super().__init__()
        self._dbc_files : list[DBCFile] = []
        self._current_dbc_file : DBCFile | None = None

    # === FROM File CONTROL ===

    # Model에 파일 추가
    def add_file(self, dbc_file : DBCFile):
        # 중복 확인 
        if dbc_file.file_path in [f.file_path for f in self._dbc_files]:
            return
        
        # 추가
        self._dbc_files.append(dbc_file)
        
        # 선택 파일 변경
        self._current_dbc_file = dbc_file

        #log 
        print("Model : add_file")

        # emit 
        self.files_changed.emit(self._get_files_names())

    # Model에 파일 제거
    def remove_file(self, dbc_file_name : str):
        
        #파일 명 탐색
        for dbc_file in self._dbc_files:

            #일치 시
            if dbc_file.file_name == dbc_file_name:
                self._dbc_files.remove(dbc_file) #제거
                self._current_dbc_file = self._dbc_files[-1] if self._dbc_files else None # 선택 파일 변경
                break #종료


        #log 
        print("File Model : remove_file")

        # emit 
        self.files_changed.emit(self._get_files_names())

    # === INTERNAL ===

    def _get_files_names(self) -> list[str]:
        return [file.file_name for file in self._dbc_files]





    def get_files(self) -> list[DBCFile]:
        return self._dbc_files
    def get_files_count(self) -> int :
        return len(self._dbc_files)

    def get_current_file(self) -> DBCFile | None : 
        return self._current_dbc_file
    def set_current_file(self, dbc_file_name : str ):
        for dbc_file in self._dbc_files : 
            if dbc_file.file_name == dbc_file_name :
                self._current_dbc_file = dbc_file

        self.current_file_changed.emit(self._current_dbc_file.messages)
    def set_current_message(self, message_id : str , message_name) :
        
        for msg in self._current_dbc_file.messages :
            if msg.id == message_id :
                self.current_message_changed.emit(msg.signals)
                return