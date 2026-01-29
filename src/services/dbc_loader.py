"""
dbc_loader.py
서비스 계층: DBC 파일을 로드하고 파싱하여 도메인 모델로 변환하는 기능 제공
"""

import re
from pathlib import Path

from models.domainmodels import DBCFile, Message, Signal
from models.domainmodels.enums import ByteOrder, ValueType
from models.color_palette import pick_color


def load_dbc_file(file_path: str) -> DBCFile:
    """
    지정된 경로의 DBC 파일을 읽어 파싱하여 DBCFile 도메인 모델로 반환합니다.

    Args:
        file_path (str): DBC 파일 경로

    Returns:
        DBCFile: 파싱된 메시지/시그널 정보를 포함한 도메인 객체
    """
    # 1. 파일에서 raw content 읽기
    text = Path(file_path).read_text(encoding="utf-8")

    # 2. 메시지 및 시그널 파싱 (+ raw_lines 유지)
    raw_lines = text.splitlines()
    messages = _parse_lines(raw_lines)

    # 3. DBCFile 도메인 객체 생성 및 반환
    return DBCFile(
        file_path=file_path,
        file_name=Path(file_path).name,
        raw_content=text,
        messages=messages,
    )


def _parse_lines(raw_lines: list[str]) -> list[Message]:
    """
    raw line list에서 메시지/시그널을 파싱하고, Message 블록 범위를 기록합니다.

    Args:
        raw_lines (list[str]): DBC 파일의 raw line 리스트

    Returns:
        list[Message]: 파싱된 메시지 객체 리스트
    """
    messages: list[Message] = []
    current_message: Message | None = None
    current_signal_index: int = 0

    # line index 기반으로 BO_ 블록 범위 추적
    for i, raw in enumerate(raw_lines):
        line = raw.strip()

        # 메시지(BO_) 라인 파싱
        if line.startswith("BO_"):
            # 이전 메시지 블록의 종료 라인 기록
            if current_message is not None and current_message.block_start_line is not None:
                current_message.block_end_line_exclusive = i

            match = re.match(r"BO_\s+(\d+)\s+(\w+)\s*:\s*(\d+)\s+(\w+)", line)
            if match:
                message_id = match.group(1)
                message_name = match.group(2)
                message_length = int(match.group(3))

                current_message = Message(
                    id=message_id,
                    name=message_name,
                    length=message_length,
                    signals=[],
                    block_start_line=i,
                    block_end_line_exclusive=None,
                )
                current_signal_index = 0
                messages.append(current_message)
            else:
                # BO_ 라인이지만 파싱 실패한 경우: 블록 매핑 일관성을 위해 current_message를 끊는다.
                current_message = None

        # 시그널(SG_) 라인 파싱
        elif line.startswith("SG_") and current_message is not None:
            match = re.match(
                r"SG_\s+(\w+)\s*:\s*(\d+)\|(\d+)@(\d)([+-])\s*"
                r"\(([^,]+),([^)]+)\)\s*"
                r"\[([^\|]+)\|([^\]]+)\]\s*"
                r"\"([^\"]*)\"",
                line,
            )
            if match:
                byte_order = ByteOrder.BIG if match.group(4) == "0" else ByteOrder.LITTLE
                value_type = ValueType(match.group(5))

                signal = Signal(
                    name=match.group(1),
                    description="",
                    start_bit=int(match.group(2)),
                    length=int(match.group(3)),
                    byte_order=byte_order,
                    value_type=value_type,
                    hex_value="",
                    dec_value=0,
                    factor=float(match.group(6)),
                    offset=float(match.group(7)),
                    min=float(match.group(8)),
                    max=float(match.group(9)),
                    unit=match.group(10),
                    color=pick_color(current_signal_index),
                )
                current_message.signals.append(signal)
                current_signal_index += 1

    # 마지막 메시지 블록의 종료 라인 기록(EOF)
    if current_message is not None and current_message.block_start_line is not None:
        current_message.block_end_line_exclusive = len(raw_lines)

    return messages


# 하위호환: 기존 호출부가 있을 수 있으므로 이름 유지
def _parse_text(text: str) -> list[Message]:
    """
    DBC 텍스트에서 메시지/시그널 정보를 파싱하여 Message 객체 리스트로 반환합니다.

    Args:
        text (str): DBC 파일의 전체 텍스트

    Returns:
        list[Message]: 파싱된 메시지 객체 리스트
    """
    return _parse_lines(text.splitlines())



