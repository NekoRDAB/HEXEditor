from dataclasses import dataclass
from HexFile import HexFile


@dataclass
class ByteChange:
    position: int
    value: str


def apply_changes(hex_file: HexFile, changes: list):
    for change in changes:
        hex_file.change_byte_at(change.position, int(change.value, 16))
