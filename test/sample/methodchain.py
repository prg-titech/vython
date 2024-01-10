class Node:
    def __init__(self):
        self.next_node = None

    def link_to(self, node):
        self.next_node = node
        return node


first = Node()
second = Node()
third = Node()
first.link_to(second).link_to(third)
