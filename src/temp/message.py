from dataclasses import dataclass
from model.signal import Signal
""" 
    - Message model
"""

@dataclass
class Message : 
    id : str
    name : str
    type : str # "STANDARD" | "EXTENDED" | "FD" | "FD_EXTENDED"
    length : int
    signals : list[Signal]