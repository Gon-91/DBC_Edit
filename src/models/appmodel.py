"""
appmodel.py
-----------
앱의 전역 데이터 모델. 파일, 메시지, 시그널 등 전체 상태를 관리하며, 시그널을 통해 상태 변화를 알린다.
"""
from models.domainmodels import DBCFile, Message
from models.message_signal_model import MessageSignalModel
from PySide6.QtCore import QObject, Signal

class AppModel(QObject):
    """
    AppModel
    --------
    - 앱 전체의 파일, 메시지, 시그널 등 상태를 관리하는 전역 모델
    - 상태 변화 시 시그널을 emit하여 ViewModel/Controller에 알림
    """
    files_changed = Signal(list)         # 파일 목록 변경 시 emit
    file_selected = Signal(object)       # 파일 선택 시 emit
    message_selected = Signal(object)    # 메시지 선택 시 emit
    current_file_changed = Signal(object)    # 현재 파일 변경 시 emit
    current_message_changed = Signal(object) # 현재 메시지 변경 시 emit

    # dirty 상태 변화(선택): UI에서 Save enable, 제목 표시 등에 활용
    dirty_changed = Signal(bool)

    def __init__(self):
        """
        AppModel 생성자
        - 파일, 메시지, 시그널 등 상태 초기화
        """
        super().__init__()
        self._dbc_files: list[DBCFile] = []
        self._current_dbc_file: DBCFile | None = None
        self._current_message: Message | None = None
        self._current_signals: MessageSignalModel | None = None

        # Phase 1: saving(block patch)용 dirty 상태
        self._file_dirty: bool = False
        self._dirty_message_ids: set[str] = set()

    # === FROM File CONTROL ===
    def add_file(self, dbc_file: DBCFile):
        """
        파일 추가 및 상태/시그널 갱신
        - 중복 파일은 무시
        - 파일 추가 후 현재 파일로 설정
        - files_changed 시그널 emit
        """
        if dbc_file.file_path in [f.file_path for f in self._dbc_files]:
            return
        self._dbc_files.append(dbc_file)
        self._current_dbc_file = dbc_file
        print("Model : add_file")
        self.files_changed.emit(self._get_files_names())

    def remove_file(self, dbc_file_name: str):
        """
        파일 제거 및 상태/시그널 갱신
        - 파일 제거 후 현재 파일 재설정
        - files_changed 시그널 emit
        """
        for dbc_file in self._dbc_files:
            if dbc_file.file_name == dbc_file_name:
                self._dbc_files.remove(dbc_file)
                self._current_dbc_file = self._dbc_files[-1] if self._dbc_files else None
                break
        print("Model : remove_file")
        self.files_changed.emit(self._get_files_names())

    def select_file(self, file_name: str):
        """
        파일 선택 및 상태/시그널 갱신
        - 선택된 파일을 현재 파일로 설정
        - file_selected 시그널 emit
        """
        for dbc_file in self._dbc_files:
            if dbc_file.file_name == file_name:
                self._current_dbc_file = dbc_file
                break
        self.file_selected.emit(self._current_dbc_file.messages)
        print("Model : select_file")

    def select_message(self, select_message: Message):
        """
        메시지 선택 및 상태/시그널 갱신
        - 선택된 메시지를 현재 메시지로 설정
        - message_selected 시그널 emit
        """
        dbc_file = self._current_dbc_file
        messages = dbc_file.messages
        message = None
        for msg in messages:
            if msg.id == select_message.id and msg.name == select_message.name and msg.length == select_message.length:
                message = msg
                break
        self._current_signals = MessageSignalModel(message)

        # 현재 선택 메시지의 변경을 dirty로 추적
        self._wire_current_signal_model(self._current_signals, message)

        self.message_selected.emit(self._current_signals)
        print("Model : select_message")

    # === INTERNAL ===
    def _get_files_names(self) -> list[str]:
        """
        내부 메서드: 파일 이름 목록 반환
        """
        print("Model(internal) : _get_files_names")
        return [file.file_name for file in self._dbc_files]

    def get_files(self) -> list[DBCFile]:
        """
        파일 목록 반환
        """
        return self._dbc_files

    def get_files_count(self) -> int:
        """
        파일 개수 반환
        """
        return len(self._dbc_files)

    def get_current_file(self) -> DBCFile | None:
        """
        현재 선택된 파일 반환
        """
        return self._current_dbc_file

    def set_current_file(self, dbc_file_name: str):
        """
        현재 파일 설정 및 상태/시그널 갱신
        - current_file_changed 시그널 emit
        """
        for dbc_file in self._dbc_files:
            if dbc_file.file_name == dbc_file_name:
                self._current_dbc_file = dbc_file
        self.current_file_changed.emit(self._current_dbc_file.messages)

    def set_current_message(self, message_id: str, message_name: str):
        """
        현재 메시지 설정 및 상태/시그널 갱신
        - current_message_changed 시그널 emit
        """
        for msg in self._current_dbc_file.messages:
            if msg.id == message_id:
                self.current_message_changed.emit(msg.signals)
                return

    def set_current_dbc_file(self, dbc_file: DBCFile) -> None:
        """현재 파일 객체를 교체합니다.

        저장 후 재로드(load_dbc_file)된 객체로 교체하여,
        - Message block range(block_start_line/end) 재계산 결과를 반영하고
        - 이후 저장/patch에서 인덱스 불일치를 방지합니다.

        또한 파일 목록에 동일 file_path 항목이 있으면 함께 교체합니다.
        """
        # 파일 목록 교체
        for i, f in enumerate(self._dbc_files):
            if f.file_path == dbc_file.file_path:
                self._dbc_files[i] = dbc_file
                break

        # 현재 파일 교체
        self._current_dbc_file = dbc_file
        # UI 갱신을 위해 현재 파일 변경 시그널을 내보냄(기존 패턴 유지)
        self.current_file_changed.emit(dbc_file.messages)

    # === DIRTY (Phase 1) ===
    def is_file_dirty(self) -> bool:
        return self._file_dirty

    def dirty_message_ids(self) -> set[str]:
        # 외부에서 수정하지 못하도록 복사본 반환
        return set(self._dirty_message_ids)

    def clear_dirty(self) -> None:
        self._dirty_message_ids.clear()
        self._set_file_dirty(False)

    def mark_message_dirty(self, message_id: str) -> None:
        self._dirty_message_ids.add(str(message_id))
        self._set_file_dirty(True)

    def _set_file_dirty(self, dirty: bool) -> None:
        if self._file_dirty == dirty:
            return
        self._file_dirty = dirty
        self.dirty_changed.emit(dirty)

    def _wire_current_signal_model(self, signal_model: MessageSignalModel, message: Message) -> None:
        """현재 선택된 메시지에 대해 signal 변경을 message dirty로 승격."""

        # 기존 연결이 남아있을 수 있으므로 최대한 정리
        try:
            signal_model.signal_updated.disconnect()
        except (TypeError, RuntimeError):
            pass
        try:
            signal_model.signal_changed.disconnect()
        except (TypeError, RuntimeError):
            pass

        def _on_any_change(*_args):
            self.mark_message_dirty(message.id)

        signal_model.signal_updated.connect(_on_any_change)
        signal_model.signal_changed.connect(_on_any_change)