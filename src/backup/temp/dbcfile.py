from dataclasses import dataclass
from model.message import Message
from model.signal import Signal


"""
     - DBC File Model. 

"""

@dataclass
class DBCFile:
    file_path : str
    file_name : str
    raw_content : str
    messages : list[Message]
    #signals : list[Signal]