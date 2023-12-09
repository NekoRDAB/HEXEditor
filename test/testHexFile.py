import random
import unittest
from collections import deque
from HexFile import open_hex, BytePage, HexFile


class testHexFile(unittest.TestCase):

    def test_simple_read(self):
        with open_hex('test/test_files/simple_file.txt') as f:
            expected = ('A'*f.PAGE_SIZE).encode(encoding='ascii')
            self.assertEqual(f.get_next_bytes(), BytePage(0, expected))

    def test_multiple_read(self):
        page_count = 7
        expected = bytearray(random.randint(0, 255)
                             for _ in range(page_count*HexFile.PAGE_SIZE))
        with open('test/test_files/test_multiple_file.txt', 'wb') as f:
            f.write(expected)

        with open_hex('test/test_files/test_multiple_file.txt') as f:
            for i in range(0, page_count, f.PAGE_SIZE):
                self.assertEqual(f.get_next_bytes(),
                                 BytePage(i // f.PAGE_SIZE, expected[i:i+f.PAGE_SIZE]))

    def check_both_directions(self, filename, expected):
        forward_read_data = []
        backwards_read_data = deque()
        page_count = 0
        page_size = 0
        with open_hex(filename) as f:
            page_size = f.PAGE_SIZE
            while not f.is_eof():
                forward_read_data.extend(f.get_next_bytes().values)
                page_count += 1
            for _ in range(page_count-1):
                backwards_read_data.extendleft(
                    reversed(f.get_prev_bytes().values))

        self.assertSequenceEqual(expected, forward_read_data)
        last_page_start = len(expected) - len(expected) % 256
        self.assertSequenceEqual(
            expected[:last_page_start], backwards_read_data)

    def test_next_and_prev_work_together(self):
        expected_len = 2048
        expected = bytearray(random.randint(0, 255)
                             for _ in range(expected_len))
        filename = 'test/test_files/test_multiple_file.txt'
        with open(filename, 'wb') as f:
            f.write(expected)
        self.check_both_directions(filename, expected)

    def test_prev_zero_page_returns_first_page(self):
        with open_hex('test/test_files/simple_file.txt') as f:
            expected = ('A'*f.PAGE_SIZE).encode(encoding='ascii')
            self.assertEqual(f.get_prev_bytes(), BytePage(0, expected))

    def test_next_page_after_last_returns_last_page(self):
        with open_hex('test/test_files/simple_file.txt') as f:
            expected = None
            while not f.is_eof():
                expected = f.get_next_bytes()
            self.assertEqual(f.get_next_bytes(), expected)

    def test_when_page_len_less_than_default(self):
        for _ in range(20):
            page_count = random.randint(0, 10)
            byte_count = random.randint(1, 254)
            total_byte_count = page_count*HexFile.PAGE_SIZE + byte_count
            data = bytearray(random.randint(0, 255)
                             for _ in range(total_byte_count))
            filename = 'test/test_files/small_file.txt'
            with open(filename, 'wb') as f:
                f.write(data)
            self.check_both_directions(filename, data)
