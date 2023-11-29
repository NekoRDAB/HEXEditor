import tkinter as tk


class UserInterface:
    def __init__(self):
        self.window: tk.Tk
        self.index_label: tk.Label
        self.offset_label: tk.Label
        self.hex_text: tk.Text
        self.ascii_text: tk.Text

    def build(self):
        self.window = tk.Tk()
        self.window.geometry("800x500")
        self.build_labels()
        self.build_text_widgets()

    def build_labels(self):
        indices = []
        for i in range(16):
            hex_index = "0" + hex(i)[2:]
            indices.append(hex_index)

        offsets = []
        for i in range(16):
            hex_offset = "00" + hex(i)[2:] + "0"
            offsets.append(hex_offset)

        self.index_label = tk.Label(text=' '.join(indices), font=("Courier", 14), )
        self.offset_label = tk.Label(text='\n'.join(offsets), font=("Courier", 14))

    def build_text_widgets(self):
        self.hex_text = tk.Text(
            self.window, font=("Courier", 14)
        )
        self.ascii_text = tk.Text(
            self.window, font=("Courier", 14),
            width=16, height=16
        )

    def place_widgets(self):
        self.index_label.place(x=0, y=0)
        self.offset_label.place(x=0, y=0)
        self.window.update()
        self.index_label.place(x=self.offset_label.winfo_width(), y=0)
        self.offset_label.place(x=0, y=self.index_label.winfo_height())
        self.hex_text.place(
            x=self.offset_label.winfo_width(),
            y=self.index_label.winfo_height(),
            width=self.index_label.winfo_width(),
            height=self.offset_label.winfo_height()
        )
        self.window.update()
        self.ascii_text.place(
            x=self.hex_text.winfo_x() + self.hex_text.winfo_width() + 20,
            y=self.index_label.winfo_height()
        )

    def run(self):
        self.build()
        self.place_widgets()
        self.window.mainloop()
