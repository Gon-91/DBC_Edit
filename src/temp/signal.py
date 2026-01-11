from dataclasses import dataclass


"""
    - Signal model 
    - 
"""

@dataclass
class Signal:
    name : str  # signal name
    description : str # signal description

    byte_order : str # "BIG_ENDIAN" | "LITTLE_ENDIAN"
    start_bit : int # bit position
    length : int # length in bits

    hex_value : str # raw hex value
    dec_value : int # raw decimal value

    factor : float # scaling factor
    offset : float # offset value
    unit : str # signal unit
    
    min : float 
    max : float

    multplex : bool = False
