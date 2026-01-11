from enum import Enum


class ByteOrder(str,Enum):
    BIG = "BIG_ENDIAN"
    LITTLE = "LITTLE_ENDIAN"

class MessageType(str,Enum):
    STD = "STANDARD"
    EXTD = "EXTENDED"
    FD = "FD"
    FD_EXTD = "FD_EXTENDED"