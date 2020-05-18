"""
Kate Yurmanovych
Lesson 6 Task 3
Создать свою структуру данных Список, которая поддерживает
индексацию. Методы pop, append, insert, remove, clear. Перегрузить
операцию сложения для списков, которая возвращает новый расширенный
объект.
"""


class MyList:

    def __init__(self, size_in: int = 0):
        self._size = size_in
        self._my_list = [0] * self._size

    def __getitem__(self, index):
        return self._my_list[index]

    def __setitem__(self, index, value):
        self._my_list[index] = value

    def set_list(self, list_in):
        self._my_list = list_in[:]

    def length(self):
        len_ = 0
        for i in self._my_list:
            len_ += 1
        return len_

    # Add an item to the end of the list
    def append(self, value):
        appended_list = self._my_list[:] + [value]
        self._my_list = appended_list[:]
        return self._my_list

    # Insert an item at a given position (index of the element before which to insert)
    def insert(self, position, value):
        inserted_list = self._my_list[:position] + [value] + self._my_list[position:]
        self._my_list = inserted_list[:]
        return self._my_list

    # Remove the item at the given position in the list, and return it.
    # If no index is specified, pop() removes and returns the last item in the list
    def pop(self, position=-1):
        popped_item = self._my_list[position]
        popped_list = [item for item in self._my_list if item != popped_item]
        self._my_list = popped_list[:]
        return popped_item

    # removes the first occurrence of the element with the specified value
    def remove(self, value):
        if value in self._my_list:
            for index, item in enumerate(self._my_list):
                if item == value:
                    value_first_index = index
                    break
            new_list = [item for item in self._my_list if item != self._my_list[value_first_index]]
            self._my_list = new_list[:]
        return self._my_list

    def clear(self):
        self._my_list = []
        return self._my_list

    def __add__(self, other):
        new_mylist = MyList()
        total_list = self._my_list[:] + other[:]
        new_mylist.set_list(total_list)
        return new_mylist


if __name__ == "__main__":
    size = 5
    num_1 = 1
    num_2 = 2
    num_3 = 3
    lst1 = MyList(size)
    assert lst1.length() == size, "the size of list is incorrect"
    lst1.append(num_1)
    assert lst1.length() == size + 1, "item wasn't appended"
    assert lst1[-1] == num_1, "item wasn't appended"
    lst1[0] = num_2
    assert lst1[0] == num_2, "item wasn't set"
    lst1.insert(3, num_3)
    assert lst1[3] == num_3, "iteam wasn't inserted before the given index"
    assert lst1.pop(0) == num_2
    size_before_remove = lst1.length()
    lst1.remove(num_1)
    assert lst1.length() == size_before_remove - 1, "item was't removed"
    lst2 = MyList(size)
    new_lst = lst1 + lst2
    assert new_lst.length() == lst1.length() + lst2.length()
    assert new_lst.clear() == [], "the list wasn't cleared"
