"""
Kate Yurmanovych
Lesson 6 Task 4

2) Создать свою структуру данных Словарь, которая поддерживает методы,
get, items, keys, values. Так же перегрузить операцию сложения для
словарей, которая возвращает новый расширенный объект.
"""


class MyDict:

    def __init__(self, *args):
        if args is None:
            self._dict = {}
        else:
            self._dict = {k: v for k, v in args}

    def __getitem__(self, index):
        return self._dict[index]

    def __setitem__(self, index, value):
        self._dict[index] = value

    def set_dict(self, dict_in):
        self._dict = dict_in

    def __add__(self, other):
        new_myDict = MyDict()
        new_myDict.set_dict({**self._dict,**other._dict})
        return new_myDict


if __name__ == "__main__":
    mydict_1 = MyDict(("key1", 1), ("key2", 2))
    assert mydict_1["key1"] == 1
    mydict_1["newly added key"] = 3
    assert mydict_1["newly added key"] == 3
    mydict_2 = MyDict()
    mydict_2.set_dict({111:"value111",222:"value222"})
    added_dict = mydict_1+mydict_2
    assert type(added_dict) == MyDict

