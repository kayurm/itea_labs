"""
Kate Yurmanovych
Lesson 6 Task 1
3) Написать свой контекстный менеджер для работы с файлами.
"""


class MyFileManager:

    def __init__(self, filename:str, mode:str):
        self._filename = filename
        self._mode = mode
        self._file = None

    def __enter__(self):
        self._file = open(self._filename, self._mode)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()


if __name__ == "__main__":
    with MyFileManager("file1.txt", "w") as file:
        file.write("Some test lines\n"*10)

    with MyFileManager("file1.txt", "r") as file:
        print(file.read())