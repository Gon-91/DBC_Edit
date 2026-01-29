"""
messageviewdata.py
뷰모델 계층: 메시지 뷰 데이터 구조체
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MessageViewData:
    """
    메시지 뷰에 표시할 데이터 구조체
    """
    id: str      # 메시지 ID
    name: str    # 메시지 이름
    length: int  # 메시지 길이
