import unittest
import random
from byte_change import ByteChange, apply_changes
from HexFile import open_hex


class TestApplyChanges(unittest.TestCase):

    def testChangesApply(self):
        data = bytearray((random.randint(0, 255) for _ in range(500)))
        with open('test/test_files/test.bin', 'wb') as f:
            f.write(data)
        changes_list = []
        change_count = random.randint(1, 50)
        change_indexes = (random.randint(0, len(data) - 1)
                          for _ in range(change_count))
        for index in change_indexes:
            change_byte = random.randint(0, 255)
            changes_list.append(ByteChange(index, f'{change_byte:02x}'))
            data[index] = change_byte
        with open_hex('test/test_files/test.bin') as f:
            apply_changes(f, changes_list)
        with open('test/test_files/test.bin', 'rb') as f:
            self.assertSequenceEqual(data, f.read())
