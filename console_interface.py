import os
from HexFile import HexFile
from command_handler import CommandHandler


class ConsoleInterface:
    def __init__(self):
        self.create_variables()

    def create_variables(self):
        self.hex_file: HexFile
        self.command_handler: CommandHandler
        self.index_label: str
        self.offset_label: str
        self.hex_text: list
        self.ascii_text: list
        self.file: HexFile

    def create_labels(self, segment_index: int):
        self.index_label = " " * 8 + ' '.join([f"{index:02x}" for index in range(16)])
        self.offset_label = [f"{segment_index:06x}{offset:x}0" for offset in range(16)]

    def create_hex_text(self, byte_segment: list):
        self.hex_text = [""]*16
        for byte_index in range(len(byte_segment)):
            line = byte_index // 16
            self.hex_text[line] += " " + byte_segment[byte_index]

    def create_ascii_text(self, byte_segment: list):
        self.ascii_text = [""]*16
        for byte_index in range(len(byte_segment)):
            line = byte_index // 16
            self.ascii_text[line] += self.convert_to_readable(byte_segment[byte_index])

    @staticmethod
    def convert_to_readable(byte):
        ascii_code = int(byte, base=16)
        if 32 <= ascii_code <= 126:
            return chr(ascii_code)
        return '.'

    def output_text(self):
        os.system('cls')
        print(self.index_label)
        for line_index in range(16):
            print(f"{self.offset_label[line_index]}{self.hex_text[line_index]}  {self.ascii_text[line_index]}")

    def open_file(self, hex_file: HexFile):
        self.hex_file = hex_file
        byte_page = hex_file.get_next_bytes()
        segment_index = byte_page.index
        byte_array = byte_page.values
        byte_segment = [f"{byte:02x}" for byte in byte_array]
        self.create_labels(segment_index)
        self.create_hex_text(byte_segment)
        self.create_ascii_text(byte_segment)
        self.output_text()

    def next(self):
        byte_page = self.hex_file.get_next_bytes()
        byte_array = byte_page.values
        byte_segment = [f"{byte:02x}" for byte in byte_array]
        segment_index = byte_page.index
        self.create_labels(segment_index)
        self.create_hex_text(byte_segment)
        self.create_ascii_text(byte_segment)
        self.output_text()

    def prev(self):
        byte_page = self.hex_file.get_prev_bytes()
        byte_array = byte_page.values
        byte_segment = [f"{byte:02x}" for byte in byte_array]
        segment_index = byte_page.index
        self.create_labels(segment_index)
        self.create_hex_text(byte_segment)
        self.create_ascii_text(byte_segment)
        self.output_text()

    def run(self):
        self.command_handler = CommandHandler(self)
        command = input()
        while command != "exit":
            self.command_handler.execute_command(command.split())
            command = input()
