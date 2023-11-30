class ByteChanger:
    @staticmethod
    def hex_input_to_bytes(text: str):
        if not ByteChanger.is_correct_text(text):
            return False, None
        return True, ''.join(text.split())

    @staticmethod
    def is_correct_byte(byte: str):
        hex_digits = ([str(i) for i in range(10)]
                      + [chr(ord('a') + i) for i in range(6)])
        if len(byte) == 2:
            if byte[0] in hex_digits and byte[1] in hex_digits:
                return True
        return False

    @staticmethod
    def is_correct_text(text: str):
        parts = text.split()
        for byte in parts:
            if not ByteChanger.is_correct_byte(byte):
                return False
        return True
