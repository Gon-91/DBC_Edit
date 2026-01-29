"""dbc_writer.py

서비스 계층: DBC 저장(쓰기) 기능.

Decision 002에 따른 저장 전략:
- 원본 텍스트를 최대한 보존한다.
- 단, "dirty"로 표시된 Message 블록(BO_ ~ next BO_) 내부는 canonical 포맷으로 재생성하여 교체한다.

현재 Phase 1 범위(MVP):
- "현재 파싱된 Message 객체"로부터 블록 텍스트를 생성한다.
- 원본 파일(raw_lines)에 대해, 지정된 message_id들의 블록 범위만 patch 적용해 최종 저장 텍스트를 만든다.

주의:
- 이 모듈은 아직 file I/O(atomic save)는 다루지 않는다. (Phase 1-2/1-3에서 연결)
"""

""" Call Graph
build_text_with_patches(dbc_file, dirty_message_ids)
  ├─ raw_lines = dbc_file.raw_content.splitlines()
  └─ apply_message_block_patches(raw_lines, dbc_file.messages, dirty_message_ids)
       ├─ (범위 검증: Message.block_start_line / block_end_line_exclusive)
       ├─ for each target Message (역순):
       │    └─ build_message_block_lines(message)
       │         ├─ format_bo_line(message)
       │         └─ for each Signal:
       │              └─ format_sg_line(signal)
       │                   ├─ _byte_order_token(byte_order)
       │                   └─ _value_type_token(value_type)
       └─ return PatchResult(patched_text, patched_lines)
"""


from dataclasses import dataclass
from typing import Iterable, Sequence

from models.domainmodels import DBCFile, Message, Signal
from models.domainmodels.enums import ByteOrder, ValueType


# ====== Formatting (Decision 002 canonical templates) ======

def format_bo_line(message: Message) -> str:
    """BO_ 라인 canonical 포맷.

    Canonical:
        BO_ {message_id} {message_name}: {dlc} {sender}

    Note:
        현재 도메인 `Message`에 sender가 없으므로, MVP에서는 송신자를 `Vector__XXX`로 고정.
        (추후 Message 모델에 sender를 추가하거나 원본에서 추출해 보존 가능)
    """

    sender = getattr(message, "sender", None) or "Vector__XXX"
    return f"BO_ {message.id} {message.name}: {message.length} {sender}"


def format_sg_line(signal: Signal) -> str:
    """SG_ 라인 canonical 포맷.

    Canonical structure:
        SG_ {signal_name} : {start}|{length}@{byte_order}{value_type} ({factor},{offset}) [{min}|{max}] "{unit}" {receivers}

    MVP 제약:
        - receivers 정보는 현재 모델에 없으므로 생략한다.
        - description, multiplex 등도 아직 반영하지 않는다.
    """

    unit = signal.unit or ""

    # Enum 타입이 아닐 가능성(레거시)을 방어적으로 캐스팅
    byte_order = signal.byte_order if isinstance(signal.byte_order, ByteOrder) else ByteOrder(str(signal.byte_order))
    value_type = signal.value_type if isinstance(signal.value_type, ValueType) else ValueType(str(signal.value_type))

    return (
        f"SG_ {signal.name} : "
        f"{signal.start_bit}|{signal.length}@{_byte_order_token(byte_order)}{_value_type_token(value_type)} "
        f"({signal.factor},{signal.offset}) "
        f"[{signal.min}|{signal.max}] "
        f"\"{unit}\""
    )

# ----- formatted helpers -----


def _byte_order_token(byte_order: ByteOrder) -> str:
    # DBC: @0 = Motorola(Big Endian), @1 = Intel(Little Endian)
    return "0" if byte_order == ByteOrder.BIG else "1"


def _value_type_token(value_type: ValueType) -> str:
    # ValueType enum은 '+/-'를 그대로 value로 갖는다.
    return value_type.value




# ====== Message block builder ======

def build_message_block_lines(message: Message) -> list[str]:
    """Message 1개를 canonical 텍스트 라인 리스트로 생성."""

    lines: list[str] = [format_bo_line(message)]
    for sig in message.signals:
        lines.append(format_sg_line(sig))
    return lines





# ====== Patch ======
# DBCFile.raw_content 기준으로, dirty message 블록만 교체하는 기능.

@dataclass(frozen=True)
class PatchResult:
    patched_text: str # 전체 교체 완료된 텍스트
    patched_lines: list[str] # 전체 교체 완료된 라인 리스트


def apply_message_block_patches(
    raw_lines: Sequence[str],             
    messages: Sequence[Message],
    dirty_message_ids: Iterable[str],
) -> PatchResult:
    """원본 라인(raw_lines)에 대해 dirty message 블록만 교체하여 결과를 만든다.

    Args:
        raw_lines: 원본 파일을 splitlines() 한 리스트
        messages: 파싱된 메시지 목록(각 message는 block_start_line/block_end_line_exclusive 보유)
        dirty_message_ids: 교체 대상 message.id 목록

    Returns:
        PatchResult: 교체 완료된 텍스트/라인

    Raises:
        ValueError: 블록 범위가 누락/비정상인 dirty message가 포함된 경우
    """

    dirty = set(dirty_message_ids)
    # patch 대상 메시지만 추출 후, start line 기준으로 정렬(아래에서 역순 치환하려고)
    targets: list[Message] = [m for m in messages if m.id in dirty]

    # 범위 검증
    for m in targets:
        if m.block_start_line is None or m.block_end_line_exclusive is None:
            raise ValueError(f"Message {m.id} has no block range mapping")
        if m.block_end_line_exclusive < m.block_start_line:
            raise ValueError(
                f"Message {m.id} has invalid block range: "
                f"{m.block_start_line}..{m.block_end_line_exclusive}"
            )

    # 안전한 in-place 치환을 위해 start index 내림차순으로 처리
    targets.sort(key=lambda m: m.block_start_line or -1, reverse=True)

    patched = list(raw_lines)
    for m in targets:
        start = int(m.block_start_line)
        end = int(m.block_end_line_exclusive)
        replacement = build_message_block_lines(m)
        patched[start:end] = replacement

    return PatchResult(patched_text="\n".join(patched) + ("\n" if raw_lines and raw_lines[-1].endswith("\n") else ""), patched_lines=patched)


def build_text_with_patches(dbc_file: DBCFile, dirty_message_ids: Iterable[str]) -> str:
    """DBCFile(raw_content) 기준으로 dirty messages만 patch해서 저장 텍스트를 만든다."""

    raw_lines = dbc_file.raw_content.splitlines()
    result = apply_message_block_patches(raw_lines, dbc_file.messages, dirty_message_ids)
    return result.patched_text
