import random
import unittest
from HexFile import open_hex, BytePage


class testHexFile(unittest.TestCase):

    def test_simple_read(self):
        with open_hex('test/test_files/simple_file.txt') as f:
            expected = ('A'*256).encode(encoding='ascii')
            self.assertEqual(f.get_next_bytes(), BytePage(0, expected))

    def test_multiple_read(self):
        expected = bytearray(random.randint(0, 255) for _ in range(2048))
        with open('test/test_files/test_multiple_file.txt', 'wb') as f:
            f.write(expected)

        with open_hex('test/test_files/test_multiple_file.txt') as f:
            for i in range(0, 2048, 256):
                self.assertEqual(f.get_next_bytes(),
                                 BytePage(i // 256, expected[i:i+256]))

    def test_next_and_prev_work_together(self):
        pages_count = 5
        expected = bytearray(random.randint(0, 255)
                             for _ in range(pages_count*256))
        with open('test/test_files/test_multiple_file.txt', 'wb') as f:
            f.write(expected)
        forward_read_data = []
        backwards_read_data = []
        with open_hex('test/test_files/test_multiple_file.txt') as f:
            for _ in range(pages_count):
                forward_read_data.extend(f.get_next_bytes().values)
            for _ in range(pages_count-1):
                backwards_read_data.extend(reversed(f.get_prev_bytes().values))
        self.assertSequenceEqual(expected, forward_read_data)
        self.assertSequenceEqual(expected[:-256], backwards_read_data[::-1])

    def test_prev_zero_page_returns_first_page(self):
        with open_hex('test/test_files/simple_file.txt') as f:
            expected = ('A'*256).encode(encoding='ascii')
            self.assertEqual(f.get_prev_bytes(), BytePage(0, expected))

    def test_next_page_after_last_returns_last_page(self):
        with open_hex('test/test_files/simple_file.txt') as f:
            expected = None
            while not f.is_eof():
                expected = f.get_next_bytes()
            self.assertEqual(f.get_next_bytes(), expected)
