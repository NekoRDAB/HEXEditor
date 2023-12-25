from byte_change import ByteChange, apply_changes
from HexFile import HexFile, open_hex, get_path


class Command:
    def __init__(self, method: callable, usage: str):
        self.method = method
        self.usage = usage

    def __call__(self, args: list):
        self.method(args)

    def print_usage(self):
        print(f"Usage: {self.usage}")


class CommandHandler:
    def __init__(self, interface):
        self.interface = interface
        self.commands = dict()
        self.change_list = []
        self.register_commands()

    def register_commands(self):
        self.commands["change"] = Command(
            self.change, "change {byte|symbol} {position} {XX|symbol}"
        )
        self.commands["open"] = Command(
            self.open, "open {file_name}"
        )
        self.commands["next"] = Command(
            self.next, "next"
        )
        self.commands["prev"] = Command(
            self.prev, "prev"
        )
        self.commands["save"] = Command(
            self.save, "save"
        )

    def execute_command(self, args: list):
        if len(args) == 0:
            print("Expected command")
            return None
        command = args[0]
        if command not in self.commands:
            print(f"Unknown command: {command}")
            return None
        self.commands[command](args)

    def change(self, args: list):
        if len(args) < 4:
            self.commands["change"].print_usage()
            return None
        if args[1] == "byte":
            self.change_byte(args)
        elif args[1] == "symbol":
            self.change_symbol(args)
        else:
            self.commands["change"].print_usage()

    def change_byte(self, args: list):
        position = self.parse_position_from_args(args)
        if position == -1 or not self.is_byte(args[3]):
            self.commands["change"].print_usage()
            return None
        self.change_list.append(ByteChange(position, args[3]))

    def change_symbol(self, args: list):
        position = self.parse_position_from_args(args)
        if position == -1 or len(args[3]) != 1:
            self.commands["change"].print_usage()
            return None
        ascii_code = ord(args[3])
        byte_value = f"{ascii_code:02x}"
        self.change_list.append(ByteChange(position, byte_value))

    def open(self, args):
        if len(args) != 2:
            self.commands["open"].print_usage()
            return None
        filename = args[1]
        path = get_path(filename)
        hex_file = HexFile(path)
        self.interface.open_file(hex_file)

    def next(self, args):
        if len(args) != 1:
            self.commands["next"].print_usage()
            return None
        self.interface.next()

    def prev(self, args):
        if len(args) != 1:
            self.commands["prev"].print_usage()
            return None
        self.interface.prev()

    def save(self, args):
        if len(args) != 1:
            self.commands["save"].print_usage()
            return None
        file = self.interface.hex_file
        apply_changes(file, self.change_list)
        path = file.path
        file.close()
        self.interface.open_file(HexFile(path))

    @staticmethod
    def is_byte(value: str) -> bool:
        digits = [f"{i:x}" for i in range(16)]
        if len(value) == 2 and value[0] in digits and value[1] in digits:
            return True
        return False

    @staticmethod
    def parse_position_from_args(args: list) -> int:
        try:
            position = int(args[2], base=16)
            return position
        except ValueError:
            print(f"Wrong position: {args[2]}")
            return -1
