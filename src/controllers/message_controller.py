"""
message_controller.py
---------------------
메시지 관련 컨트롤러. 메시지 선택 등 메시지 관리 기능을 제공한다.
"""

class MessageController:
    """
    MessageController
    -----------------
    - 메시지 선택 등 메시지 관리 기능 제공
    """
    def __init__(self, data_model):
        """
        메시지 컨트롤러 생성자
        :param data_model: 앱의 데이터 모델
        """
        self.model = data_model

    def select_message(self, selected_message):
        """
        메시지 선택 처리
        """
        self.model.select_message(selected_message)