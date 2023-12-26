import random
import unittest
from HexFile import HexFileStack, PAGE_SIZE


class testHexFileStack(unittest.TestCase):

    def testEmptyStackPopFails(self):
        stack = HexFileStack('test.bin')
        self.assertRaises(IndexError, stack.pop)

    def testPushAndPop(self):
        stack = HexFileStack('test.bin')
        data = random.randbytes(PAGE_SIZE)
        stack.push(data)
        self.assertEqual(data, stack.pop())
        self.assertRaises(IndexError, stack.pop)

    def testPushNotFullPage(self):
        stack = HexFileStack('test.bin')
        data = random.randbytes(random.randint(1, PAGE_SIZE-2))
        stack.push(data)
        self.assertEquals(data, stack.pop())
        self.assertRaises(IndexError, stack.pop)

    def testPushMultiplePages(self):
        stack = HexFileStack('test.bin')
        expected = []
        page_count = random.randint(2, 10)
        for _ in range(page_count):
            current_page = random.randbytes(PAGE_SIZE)
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
            current_page = random.randbytes(random.randint(1, PAGE_SIZE-1))
            expected.extend(current_page)
            stack.push(current_page, trim=True)
        actual_data = []
        while not stack.is_empty():
            actual_data.append(stack.pop())
        for i in range(0, len(expected), PAGE_SIZE):
            if i == 0:
                current_expected = expected[-i-PAGE_SIZE:]
            else:
                current_expected = expected[-i-PAGE_SIZE:-i]
            current_actual_data = actual_data[i//256]
            self.assertSequenceEqual(current_expected, current_actual_data)
        self.assertRaises(IndexError, stack.pop)
