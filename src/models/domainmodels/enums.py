"""
enums.py
--------
CAN 메시지/시그널 관련 Enum 정의 (ByteOrder, MessageType 등)
"""
from enum import Enum

class ByteOrder(str, Enum):
    """
    ByteOrder
    ---------
    - 바이트 오더(엔디안) 구분 Enum
    """
    BIG = "BIG_ENDIAN"
    LITTLE = "LITTLE_ENDIAN"

class MessageType(str, Enum):
    """
    MessageType
    -----------
    - 메시지 타입 구분 Enum
    """
    STD = "STANDARD"
    EXTD = "EXTENDED"
    FD = "FD"
    FD_EXTD = "FD_EXTENDED"

class ValueType(str, Enum):
    """
    CAN Signal ValueType
    -----------
    - 시그널 부호 구분 Enum
    - signed / unsigned / IEEE float / IEEE double
    """

    UNSIGNED = "+"
    SIGNED = "-"
    #IEEE_FLOAT = "IEEE_FLOAT"
    #IEEE_DOUBLE = "IEEE_DOUBLE"