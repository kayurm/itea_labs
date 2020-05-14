"""Kateryna Yurmanovych
     lesson 3
     Homework - Queue class (FIFO)
"""
import queue


class Que:

    def __init__(self, queue_size: int = 0):
        self.queue_size = queue_size
        self.queue_ = queue.Queue(maxsize=self.queue_size)

    def is_empty(self):
        # returns True if empty
        return self.queue_.empty()

    def add_item(self, item):
        if not self.queue_.full():
            self.queue_.put(item)
            print(f'The item "{item}" was added')
        else:
            print(f"The queue is full, item '{item}' was not added")

    # removes and returns the item from the queue's head
    def pop_item(self):
        return self.queue_.get() if not self.queue_.empty() else None

    def print_queue(self):
        print("The queue is:", list(self.queue_.queue))


if __name__ == "__main__":
    my_queue = Que(3)
    my_queue.add_item(1)
    my_queue.add_item(2)
    my_queue.add_item(3)
    my_queue.add_item(4)
    my_queue.print_queue()
    my_queue.pop_item()
    my_queue.print_queue()






