class LinkedList:
    def __init__(self):
        self.head: Node = None
        self.tail: Node = None

    def insert(self, node, index: int):
        pass

    def add_to_end(self, value, index):
        if not self.head:
            self.head = Node(value, None, None, index)
            self.tail = self.head
        else:
            pass


class Node:
    def __init__(self, value, prev, next, index):
        self.value = value
        self.prev = prev
        self.next = next
        self.index = index
