from dataclasses import dataclass
from HexFile import HexFile

@dataclass
class ByteChange:
    position: int
    value: str
