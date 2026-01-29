"""
signalviewdata.py
뷰모델 계층: 시그널 뷰 데이터 구조체
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class SignalViewData:
    """
    시그널 뷰에 표시할 데이터 구조체
    """
    color: str      # 시그널 색상
    name: str       # 시그널 이름
    start_bit: int  # 시작 비트
    length: int     # 길이
    factor: int     # 팩터
    offset: int     # 오프셋
    unit: str       # 단위
    min: int        # 최소값
    max: int        # 최대값
    byte_order: str # 바이트 오더
    sign: str       # '+'(unsigned) | '-'(signed)