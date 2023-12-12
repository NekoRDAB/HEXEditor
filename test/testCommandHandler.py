import unittest
from command_handler import CommandHandler
from byte_change import ByteChange


class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.cmd_handler = CommandHandler()

    def test_change_byte_correct(self):
        args = "change byte 255 ff"
        expected = ByteChange(255, "ff")
        actual = self.cmd_handler.change_byte(args.split())
        self.assertEqual(expected, actual)

    def test_change_byte_wrong_position(self):
        args = "change byte beef ff"
        self.assertRaises(ValueError, lambda: self.cmd_handler.change_byte(args.split()))

    def test_change_byte_wrong_value(self):
        args = "change byte 255 value"
        self.assertRaises(ValueError, lambda: self.cmd_handler.change_byte(args.split()))

    def test_change_symbol_correct(self):
        args = "change symbol 255 A"
        expected = ByteChange(255, f'{ord("A"):02x}')
        actual = self.cmd_handler.change_symbol(args.split())
        self.assertEqual(expected, actual)

    def test_change_symbol_wrong_position(self):
        args = "change symbol beef A"
        self.assertRaises(ValueError, lambda: self.cmd_handler.change_symbol(args.split()))

    def test_change_symbol_wrong_value(self):
        args = "change byte 255 value"
        self.assertRaises(ValueError, lambda: self.cmd_handler.change_symbol(args.split()))

    def test_change_correct(self):
        args = "change byte 255 ff"
        expected = ByteChange(255, "ff")
        self.cmd_handler.change(args.split())
        actual = self.cmd_handler.change_list[0]
        self.assertEqual(expected, actual)

        args = "change symbol 255 A"
        expected = ByteChange(255, f'{ord("A"):02x}')
        self.cmd_handler.change(args.split())
        actual = self.cmd_handler.change_list[1]
        self.assertEqual(expected, actual)

    def test_change_less_arguments(self):
        args = "change byte"
        self.assertRaises(ValueError, lambda: self.cmd_handler.change(args.split()))

    def test_change_unknown_argument(self):
        args = "change something 255 ff"
        self.assertRaises(ValueError, lambda: self.cmd_handler.change(args.split()))


if __name__ == '__main__':
    unittest.main()
