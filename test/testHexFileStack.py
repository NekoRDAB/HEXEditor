import random
import unittest
from HexFile import HexFileStack


class testHexFileStack(unittest.TestCase):

    def testEmptyStackPopFails(self):
        stack = HexFileStack('test.bin')
        self.assertRaises(IndexError, stack.pop)

    def testPushAndPop(self):
        stack = HexFileStack('test.bin')
        data = random.randbytes(256)
        stack.push(data)
        self.assertEquals(data, stack.pop())
        self.assertRaises(IndexError, stack.pop)

    def testPushNotFullPage(self):
        stack = HexFileStack('test.bin')
        data = random.randbytes(random.randint(1, 254))
        stack.push(data)
        self.assertEquals(data, stack.pop())
        self.assertRaises(IndexError, stack.pop)

    def testPushMultiplePages(self):
        stack = HexFileStack('test.bin')
        expected = []
        page_count = random.randint(2, 10)
        for _ in range(page_count):
            current_page = random.randbytes(256)
            expected.append(current_page)
            stack.push(current_page)
        actual_data = []
        while not stack.is_empty():
            actual_data.append(stack.pop())
        self.assertSequenceEqual(expected, actual_data[::-1])
        self.assertRaises(IndexError, stack.pop)

    def testPushWithNotFullPages(self):
        stack = HexFileStack('test.bin')
        expected = bytearray()
        page_count = random.randint(2, 10)
        for _ in range(page_count):
            current_page = random.randbytes(random.randint(1, 255))
            expected.extend(current_page)
            stack.push(current_page)
        actual_data = []
        while not stack.is_empty():
            actual_data.append(stack.pop())
        for i in range(0, len(expected), 256):
            self.assertEquals(expected[i: i + 256], actual_data[-(i//256 + 1)])
        self.assertRaises(IndexError, stack.pop)
