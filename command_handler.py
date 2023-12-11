from byte_changer import ByteChanger


class CommandHandler:
    def __init__(self):
        self.commands = dict()
        self.change_list = []

    def register_commands(self):
        self.commands["change"] = self.change

    def change(self, args):
        if len(args) <= 4:
            raise ValueError(
                "Expected \"change {byte|symbol} {position} {value}\""
            )
        if args[1] == "byte":
            self.change_byte(args)
        elif args[1] == "symbol":
            self.change_symbol(args)
        else:
            raise ValueError(
                f"Unknown argument for \"change\": {args[1]}"
            )

    def change_byte(self, args):
        try:
            position = int(args[2])
        except ValueError:
            raise ValueError(f"Wrong position: {args[2]}")
        if not self.is_byte(args[3]):
            raise ValueError(f"Wrong value to replace a byte: {args[3]}")
        self.change_list.append(ByteChanger(position, args[3]))

    def change_symbol(self, args):
        pass

    @staticmethod
    def is_byte(value):
        digits = [f"{i:x}" for i in range(16)]
        if len(value) == 2 and value[0] in digits and value[1] in digits:
            return True
        return False
