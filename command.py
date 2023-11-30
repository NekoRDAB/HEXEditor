class Command:
    def __init__(self, text: str):
        self.text = text

    def perform(self):
        raise NotImplementedError()


class ApplyChangesBytesCommand(Command):
    def __init__(self):
        super().__init__("Apply changes")

    def perform(self):
        raise NotImplementedError()
