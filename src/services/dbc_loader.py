import re

from models.domainmodels import DBCFile, Message, Signal


def load_dbc_file(file_path: str ) -> DBCFile :

    # 1. raw content 일기
    with open(file_path,"r") as file : 
        text = file.read()
        lines = file.readlines()
    
    # 2. message and signal parsing
    messages = _parser_text(text)

    # 3. Data Create 
    return DBCFile(
        file_path = file_path,
        file_name = file_path.split("/")[-1],
        raw_content= "".join(lines),
        messages = messages
    )


def _parser_text(text: str) -> list[Message]: 

    messages : list[Message] = []
    current_message : Message | None = None

    for line in text.splitlines() :
        line = line.strip() 

        # -------------------------
        # Message (BO_)
        # -------------------------
        if line.startswith("BO_"):        
            match = re.match(r"BO_\s+(\d+)\s+(\w+)\s*:\s*(\d+)\s+(\w+)",line)
            if match : 
                message_id = match.group(1)
                message_name = match.group(2)
                message_length = int(match.group(3))

                current_message = Message(
                    id = message_id,
                    name = message_name,
                    length= message_length,
                    signals= []
                )
                messages.append(current_message)

        # -------------------------
        # Signal (SG_)
        # -------------------------

        elif line.startswith("SG_") and current_message is not None:
            match = re.match(
                r"SG_\s+(\w+)\s*:\s*(\d+)\|(\d+)@(\d)([+-])\s*"
                r"\(([^,]+),([^)]+)\)\s*"
                r"\[([^\|]+)\|([^\]]+)\]\s*"
                r"\"([^\"]*)\"",
                line
            )
            if match:
                signal = Signal(
                    name=match.group(1),
                    description="",
                    start_bit=int(match.group(2)),
                    length=int(match.group(3)),
                    byte_order="BIG_ENDIAN" if match.group(4) == "0" else "LITTLE_ENDIAN",
                    hex_value="",
                    dec_value=0,
                    factor=float(match.group(6)),
                    offset=float(match.group(7)),
                    min=float(match.group(8)),
                    max=float(match.group(9)),
                    unit=match.group(10),
                )
                current_message.signals.append(signal)
    return messages            



