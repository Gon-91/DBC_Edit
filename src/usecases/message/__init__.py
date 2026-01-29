"""
message/__init__.py
유스케이스 계층: 메시지 선택 유스케이스 정의
"""
from usecases.base import Usecase

class Select(Usecase):
    """
    메시지 선택 유스케이스. 메시지 뷰 데이터를 받아 컨트롤러에 선택 요청을 전달합니다.
    """
    def __init__(self, controller):
        self._controller = controller

    def execute(self, message_view_data) -> None:
        self._controller.select_message(message_view_data)
        # 로그 출력
        print("message Usecase : Select")
