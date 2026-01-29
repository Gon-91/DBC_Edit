"""
app_context.py
-------------
앱의 전역 컨텍스트를 구성하는 모듈. 모델, 컨트롤러, 유스케이스 계층을 생성 및 연결한다.
"""
from models.appmodel import AppModel

class AppContext:
    """
    AppContext
    -----------
    - 앱 전체에서 공유하는 모델, 컨트롤러, 유스케이스 컨텍스트를 생성 및 보관
    """
    def __init__(self):
        self.model = AppModel()  # 앱 전역 모델
        self.controllers = ControllerContext(self.model)  # 컨트롤러 계층
        self.usecases = UsecaseContext(self.controllers)  # 유스케이스 계층

from controllers.file_controller import FileController
from controllers.message_controller import MessageController

class ControllerContext:
    """
    ControllerContext
    -----------------
    - 파일/메시지 등 도메인별 컨트롤러를 생성 및 보관
    """
    def __init__(self, model):
        self.file_controller = FileController(model)      # 파일 컨트롤러
        self.message_controller = MessageController(model) # 메시지 컨트롤러
        # ... (추가 컨트롤러 확장 가능)

import usecases.file as UseCaseFile
import usecases.message as UseCaseMessage

class UsecaseContext:
    """
    UsecaseContext
    --------------
    - 도메인별 유스케이스(비즈니스 로직) 객체를 생성 및 보관
    - 문자열 키로 유스케이스를 조회할 수 있음
    """
    def __init__(self, controllers):
        self._regstry = {}
        # 파일 관련 유스케이스 등록
        self._regstry["file.open"] = UseCaseFile.Open(controllers.file_controller)
        self._regstry["file.close"] = UseCaseFile.Close(controllers.file_controller)
        self._regstry["file.select"] = UseCaseFile.Select(controllers.file_controller)
        self._regstry["file.save"] = UseCaseFile.Save(controllers.file_controller)
        # 메시지 관련 유스케이스 등록
        self._regstry["message.select"] = UseCaseMessage.Select(controllers.message_controller)
    def get(self, key):
        """
        등록된 유스케이스를 키로 조회
        """
        return self._regstry[key]
