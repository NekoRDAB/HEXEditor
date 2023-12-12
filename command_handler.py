from byte_change import ByteChange


class CommandHandler:
    def __init__(self):
        self.commands = dict()
        self.change_list = []

    def register_commands(self):
        self.commands["change"] = self.change

    def execute_command(self, args: list):
        if len(args) == 0:
            raise ValueError("Expected command")
        command = args[0]
        if command not in self.commands:
            raise ValueError(f"Unknown command: {command}")
        self.commands[command](args)

    def change(self, args: list):
        if len(args) < 4:
            raise ValueError(
                "Expected \"change {byte|symbol} {position} {value}\""
            )
        if args[1] == "byte":
            self.change_list.append(self.change_byte(args))
        elif args[1] == "symbol":
            self.change_list.append(self.change_symbol(args))
        else:
            raise ValueError(
                f"Unknown argument for \"change\": {args[1]}"
            )

    def change_byte(self, args: list) -> ByteChange:
        position = self.parse_position_from_args(args)
        if not self.is_byte(args[3]):
            raise ValueError(f"Wrong value to replace a byte: {args[3]}")
        return ByteChange(position, args[3])

    def change_symbol(self, args: list) -> ByteChange:
        position = self.parse_position_from_args(args)
        if len(args[3]) != 1:
            raise ValueError(f"Wrong value to replace a symbol: {args[3]}")
        ascii_code = ord(args[3])
        byte_value = f"{ascii_code:02x}"
        return ByteChange(position, byte_value)

    @staticmethod
    def is_byte(value: str) -> bool:
        digits = [f"{i:x}" for i in range(16)]
        if len(value) == 2 and value[0] in digits and value[1] in digits:
            return True
        return False

    @staticmethod
    def parse_position_from_args(args: list) -> int:
        try:
            position = int(args[2])
        except ValueError:
            raise ValueError(f"Wrong position: {args[2]}")
        return position
