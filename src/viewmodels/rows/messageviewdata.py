from dataclasses import dataclass

@dataclass(frozen=True)
class MessageViewData:
    id: str
    name: str
    length: int
