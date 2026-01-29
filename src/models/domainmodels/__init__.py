"""
domainmodels/__init__.py
-----------------------
CAN DBC 데이터 구조의 기본 데이터 모델 정의 (Signal, Message, DBCFile 등)
"""
from dataclasses import dataclass
from models.domainmodels.enums import *
from typing import Optional

"""
    # 기본 데이터 모델들 정의
    - Signal
    - Message
    - DBCFile
"""

@dataclass
class Signal:
    """
    Signal
    ------
    - CAN 시그널(신호) 데이터 구조

    Notes:
        DBC의 SG_ 스펙에는 `@<byte_order><sign>`가 포함됩니다.
        - sign: '+'(unsigned) / '-'(signed)
    """
    name: str  # signal name
    description: str  # signal description
    byte_order: ByteOrder  # Enum "BIG_ENDIAN" | "LITTLE_ENDIAN"
    value_type: ValueType  # '+'(unsigned) | '-'(signed)
    start_bit: int  # bit position
    length: int  # length in bits
    hex_value: str  # raw hex value
    dec_value: int  # raw decimal value
    factor: float  # scaling factor
    offset: float  # offset value
    unit: str  # signal unit
    min: float
    max: float

    # UI 전용(현재 Phase): 시그널 표시용 색상. 저장 포맷(SG_)에는 아직 포함되지 않음.
    # 로더/추가 시점에서 팔레트 기반으로 기본값을 부여한다.
    color: str = ""

@dataclass
class Message:
    """
    Message
    -------
    - CAN 메시지 데이터 구조

    Notes:
        Phase 1(블록 patch 저장)을 위해, 파서가 원본 텍스트에서의 Message 블록 범위를
        `block_start_line`/`block_end_line_exclusive`에 기록할 수 있습니다.
    """
    id: str
    name: str
    # type: MessageType # Enum "STANDARD" | "EXTENDED" | "FD" | "FD_EXTENDED"
    length: int
    signals: list[Signal]

    # 원본 파일 내 BO_ 블록 범위 (line index)
    block_start_line: Optional[int] = None
    block_end_line_exclusive: Optional[int] = None

@dataclass
class DBCFile:
    """
    DBCFile
    -------
    - DBC 파일 데이터 구조
    """
    file_path: str
    file_name: str
    raw_content: str
    messages: list[Message]