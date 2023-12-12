from dataclasses import dataclass


@dataclass
class ByteChange:
    position: int
    value: str
