"""
file_controller.py
------------------
파일 관련 컨트롤러. 파일 열기/닫기/선택 등 파일 관리 기능을 제공하며, 실제 파일 파싱 등은 서비스 계층에 위임한다.
"""
from services.dbc_loader import load_dbc_file
from services.dbc_writer import build_text_with_patches

class FileController:
    """
    FileController
    --------------
    - 파일 열기/닫기/선택 등 파일 관리 기능 제공
    - SRP: 파일 읽기/쓰기 담당, 상세 파싱은 서비스 계층에 위임
    """
    def __init__(self, data_model):
        """
        파일 컨트롤러 생성자
        :param data_model: 앱의 데이터 모델
        """
        self.model = data_model

    def open_file(self, file_path: str):
        """
        파일을 열고 모델에 추가
        """
        self.model.add_file(load_dbc_file(file_path))
        print("File Controller : open_file_called")  # 로그 출력
    
    def close_file(self, file_name: str):
        """
        파일을 닫고 모델에서 제거
        """
        self.model.remove_file(file_name)
        print("File Controller : close_file_called")  # 로그 출력
    
    def select_file(self, file_name: str):
        """
        파일을 선택(활성화) 처리
        """
        self.model.select_file(file_name)
        print("File Controller : select_file_called")  # 로그 출력

    def save_file(self) -> None:
        """현재 선택된 DBC 파일을 저장합니다.

        Phase 1(MVP):
        - AppModel이 추적한 dirty message ids를 기준으로,
          원본 raw_content에 대해 dirty message 블록만 patch한 텍스트를 생성하여 저장합니다.

        Important:
        - 저장 후에는 Message 블록의 line index 매핑이 달라질 수 있으므로,
          파일을 재로드하여(block range 재계산) 메모리 모델을 동기화합니다.
        """
        dbc_file = self.model.get_current_file()
        if dbc_file is None:
            return

        dirty_ids = self.model.dirty_message_ids()
        if not dirty_ids:
            return

        patched_text = build_text_with_patches(dbc_file, dirty_ids)

        with open(dbc_file.file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(patched_text)

        # 저장 직후: 파일 재로드(블록 범위 재계산) 후 모델에 반영
        reloaded = load_dbc_file(dbc_file.file_path)

        # AppModel API가 없을 수 있으므로, 있으면 사용하고 없으면 fallback
        if hasattr(self.model, "set_current_dbc_file"):
            self.model.set_current_dbc_file(reloaded)
        else:
            self.model._current_dbc_file = reloaded  # type: ignore[attr-defined]

        # dirty clear
        self.model.clear_dirty()
        print("File Controller : save_file_called")