from dataclasses import dataclass
from models.domainmodels.enums import * 

"""
    # 기본 데이터 모델들 정의
    - Signal
    - Message
    - DBCFile
"""



@dataclass
class Signal:
    name : str  # signal name
    description : str # signal description
    byte_order : ByteOrder # Enum "BIG_ENDIAN" | "LITTLE_ENDIAN"
    start_bit : int # bit position
    length : int # length in bits
    hex_value : str # raw hex value
    dec_value : int # raw decimal value
    factor : float # scaling factor
    offset : float # offset value
    unit : str # signal unit    
    min : float 
    max : float
    #multplex : bool = False

@dataclass
class Message : 
    id : str
    name : str
    #type : MessageType # Enum "STANDARD" | "EXTENDED" | "FD" | "FD_EXTENDED"
    length : int
    signals : list[Signal]

@dataclass
class DBCFile:
    file_path : str
    file_name : str
    raw_content : str
    messages : list[Message]