from contextlib import contextmanager
from dataclasses import dataclass
import sys
import os


@dataclass
class BytePage:
    index: int
    values: bytes


class HexFile:
    PAGE_SIZE = 256

    def __init__(self, path: str) -> None:
        self.path = path
        self._file = open(path, 'r+b')
        self._cursor = 0
        self._max_position = self._file.seek(0, 2)

    def _move_cursor(self, backwards=False):
        offset = self.PAGE_SIZE
        if backwards:
            offset *= -1
        self._cursor += offset
        if self._cursor < 0:
            self._cursor = 0

    def _get_current_page(self) -> BytePage:
        self._file.seek(self._cursor)
        data = self._file.read(self.PAGE_SIZE)
        page_num = self._cursor // self.PAGE_SIZE
        return BytePage(page_num, data)

    def get_next_bytes(self) -> BytePage:
        if self.is_eof():
            self._move_cursor(backwards=True)
        page = self._get_current_page()
        self._move_cursor()
        return page

    def get_prev_bytes(self) -> BytePage:
        self._move_cursor(backwards=True)
        self._move_cursor(backwards=True)
        data = self._get_current_page()
        self._move_cursor()
        return data

    def change_byte_at(self, position: int, byte: int) -> None:
        assert 0 <= position <= self._max_position, 'Change position is out of bounds of file!'
        if position == self._max_position:
            self._max_position += 1
        self._file.seek(position)
        self._file.write(byte.to_bytes(1, "big"))

    def is_eof(self) -> bool:
        return self._cursor >= self._max_position

    def close(self) -> None:
        self._file.close()


@contextmanager
def open_hex(path: str) -> HexFile:
    full_path = get_path(path)
    hex_file = HexFile(full_path)
    try:
        yield hex_file
    finally:
        hex_file.close()


def get_path(filename: str) -> str:
    if os.path.isfile(filename):
        return filename
    filename = filename.rsplit('\\', 1)[-1]
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files or filename in dirs:
            return os.path.join(root, filename)
    sys.exit(f'File {filename} was not found!')
