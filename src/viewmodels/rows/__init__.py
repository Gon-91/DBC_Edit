from dataclasses import dataclass

@dataclass(frozen=True)
class MessageViewData:
    id: str
    name: str
    length: int


@dataclass(frozen=True)
class SignalViewData:
    color : str
    name : str
    start_bit : int
    length : int
    factor : int
    offset : int
    unit : str
    min : int
    max : int
    byte_order : str