from contextlib import contextmanager
import sys
import os

class HexFile:

    def __init__(self, path : str) -> None:
        self._file = open(path, 'r+b')
        self._cursor = self._file.seek(0)
        self._max_position = self._file.seek(0,2)
    
    def get_next_bytes(self) -> bytes:
        if self._cursor >= self._max_position:
            self._cursor -= 256
        self._file.seek(self._cursor)
        data = self._file.read(256)
        self._cursor += 256
        return data
    
    def get_prev_bytes(self) -> bytes:
        self._cursor -= 512
        if self._cursor < 0:
            self._cursor = 0
        return self.get_next_bytes()
    
    def change_byte_at(self, position : int, byte : int) -> None:
        assert 0 <= position <= self._max_position, 'Change position is out of bounds of file!'
        if position == self._max_position:
            self._max_position += 1
        self._file.seek(position)
        self._file.write(byte.to_bytes())
    
    def is_eof(self) -> bool:
        return self._cursor >= self._max_position
    
    def close(self) -> None:
        self._file.close()

@contextmanager
def open_hex(path : str) -> HexFile:
    full_path = get_path(path)
    hex_file = HexFile(full_path)
    try:
        yield hex_file
    finally:
        hex_file.close()

def get_path(filename : str) -> str:
    if os.path.isfile(filename):
        return filename
    filename = filename.rsplit('\\',1)[-1]
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files or filename in dirs:
            return os.path.join(root, filename)
    sys.exit(f'File {filename} was not found!')