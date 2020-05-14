"""Kateryna Yurmanovych
     lesson 3
     Homework - Stack class (LIFO)

I chose a deque implementation of stack.
"""
from collections import deque


class Stack:

    def __init__(self):
        self.stack = deque()

    def get_size(self):
        return len(self.stack)

    def clear(self):
        return self.stack.clear()

    def push_item(self, item):
        self.stack.append(item)

    def push_items(self, *args):
        self.stack.extend(args)

    def pop_item(self):
        return self.stack.pop() if len(self.stack) > 0 else None

    def reverse_stack(self):
        self.stack.reverse()

    def print_stack(self):
        print("The stack is:", tuple(self.stack))


if __name__ == "__main__":
    my_stack = Stack()
    my_stack.push_items(1,2,3)
    my_stack.print_stack()
    print("The stack's size is:", my_stack.get_size())
    print("Reversed and added one more item. ", end="")
    my_stack.reverse_stack()
    my_stack.push_item(4)
    my_stack.print_stack()
    my_stack.pop_item()
    my_stack.clear()
    print("Cleared stack. ", end="")
    my_stack.print_stack()















