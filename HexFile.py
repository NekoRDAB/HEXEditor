from contextlib import contextmanager
from dataclasses import dataclass
import sys
import os

PAGE_SIZE = 256


@dataclass
class BytePage:
    index: int
    values: bytes


EMPTY_PAGE = bytes(256)


class SimpleHexFile:

    def __init__(self, path: str, to_create: bool = False) -> None:
        self.path = path
        file_mode = 'w+b' if to_create else 'r+b'
        self._file = open(path, file_mode)
        self._cursor = 0
        self._max_position = self._file.seek(0, 2)

    def move_cursor(self, backwards=False):
        offset = PAGE_SIZE
        if backwards:
            offset *= -1
        self._cursor += offset
        if self._cursor < 0:
            self._cursor = 0

    def get_current_page(self) -> bytes:
        self._file.seek(self._cursor)
        data_len = min(self._max_position - self._cursor, PAGE_SIZE)
        data = self._file.read(data_len)
        return data

    def get_next_bytes(self) -> bytes:
        if self.is_eof():
            self.move_cursor(backwards=True)
        page = self.get_current_page()
        self.move_cursor()
        return page

    def get_prev_bytes(self) -> bytes:
        self.move_cursor(backwards=True)
        self.move_cursor(backwards=True)
        data = self.get_current_page()
        self.move_cursor()
        return data

    def write_data(self, data: bytes):
        if self.is_eof():
            self._file.seek(self._max_position)
        else:
            self._file.seek(self._cursor)
        self._file.write(data)
        self._max_position += max(0, self._cursor + len(data) - self._max_position)
        self._file.seek(self._cursor)

    #Сдвигает конец файла на текущее положение файла
    def truncate(self):
        self._max_position = self._cursor
    
    #Сдвигает границу текущей страницы на последний ненулевой байт
    def trim(self):
        if self._cursor > self._max_position:
            self._cursor = self._max_position

    def is_eof(self) -> bool:
        return self._cursor >= self._max_position

    def is_start(self) -> bool:
        return self._cursor == 0

    def close(self) -> None:
        self._file.close()


class HexFileStack():

    def __init__(self, path: str) -> None:
        self.path = path
        self._file = SimpleHexFile(path, to_create=True)

    def push(self, data: bytes, trim=False):
        self._file.write_data(data)
        self._file.get_next_bytes()
        if trim:
            self._file.trim()

    def pop(self) -> bytes:
        if self.is_empty():
            raise IndexError('Stack is empty')
        self._file.move_cursor(backwards=True)
        data = self._file.get_current_page()
        self._file.truncate()
        return data

    def peek(self) -> bytes:
        if self.is_empty():
            raise IndexError('Stack is empty')
        self._file.move_cursor(backwards=True)
        return self._file.get_next_bytes()

    def is_empty(self):
        return self._file.is_start()

    def close(self):
        self._file.close()


class HexFile:

    def __init__(self, path: str) -> None:
        self._source_path = path
        directory = path.rsplit('\\', maxsplit=1)[0]
        self._init_buffers(directory)
        self._source = SimpleHexFile(get_path(path), to_create=False)
        self._count = -1

    def _init_buffers(self, directory):
        self._left = HexFileStack(directory + '\\.left')
        self._right = HexFileStack(directory + '\\.right')

    def get_next_bytes(self) -> BytePage:
        if self.is_eof():
            return BytePage(self._count, self._left.peek())
        self._count += 1
        self._left.push(self._try_get_full_page())
        return BytePage(self._count, self._left.peek())
    
    def _try_get_full_page(self, initial_data : bytes=None):
        next_page = bytearray()
        if initial_data is not None:
            next_page.extend(initial_data)
        while not self.is_eof() and len(next_page) < PAGE_SIZE:
            if self._right.is_empty():
                next_page.extend(self._source.get_next_bytes())
            else:
                next_page.extend(reversed(self._right.pop()))
        if len(next_page) > PAGE_SIZE:
            self._right.push(next_page[PAGE_SIZE:][::-1], trim=True)
        return next_page[:PAGE_SIZE]

    def get_prev_bytes(self) -> BytePage:
        if self._left.is_empty():
            raise IndexError(
                'Can not return previous page, no pages read yet!')
        last_page = self._left.pop()
        if self._left.is_empty():
            self._left.push(last_page)
            return BytePage(self._count, last_page)
        self._count -= 1
        self._right.push(last_page[::-1], trim=True)
        return BytePage(self._count, self._left.peek())

    def get_current_page(self) -> BytePage:
        if self._left.is_empty():
            raise IndexError(
                'Can not return current page, no pages read yet!')
        return BytePage(self._count, self._left.peek())

    def insert(self, index, data: bytes):
        if self._left.is_empty():
            self._left.push(data)
            return
        last_page = self._left.pop()
        changed_data = last_page[:index] + data + last_page[index:]
        self._left.push(changed_data[:256])
        if len(changed_data) > 256:
            self._right.push(changed_data[256:][::-1], trim=True)

    def delete(self, index, length):
        if self._left.is_empty():
            raise IndexError(
                'Can not delete anything, no pages read yet!')
        last_page = self._left.pop()
        changed_data = last_page[:index] + last_page[index + length:]
        self._right.push(changed_data[::-1], trim=True)
        self._left.push(self._try_get_full_page())
    
    def change_byte_at(self, index : int, value : int):
        if self._left.is_empty():
            raise IndexError(
                'Can not change anything, no pages read yet!')
        page = bytearray(self._left.pop())
        page[index] = value
        self._left.push(page)

    def is_eof(self):
        return self._right.is_empty() and self._source.is_eof()

    def close(self, to_save=True) -> None:       
        if not to_save:
            return
        while not self.is_eof():
            self.get_next_bytes()
        self._source.close()
        self._right.close()
        self._left.close()
        self._source.close()
        os.remove(self._right.path)
        os.remove(self._source.path)
        os.rename(self._left.path, self._source.path)


@contextmanager
def open_hex(path: str) -> HexFile:
    full_path = get_path(path)
    hex_file = HexFile(full_path)
    try:
        yield hex_file
    finally:
        hex_file.close(to_save=True)


def get_path(filename: str) -> str:
    if os.path.isfile(filename):
        return filename
    filename = filename.rsplit('\\', 1)[-1]
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files or filename in dirs:
            return os.path.join(root, filename)
    sys.exit(f'File {filename} was not found!')