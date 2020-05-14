"""
Kateryna Yurmanovych
     lesson 5
     Task 1
Создать декоратор, который будет запускать функцию в отдельном
потоке. Декоратор должен принимать следующие аргументы:
название потока, является ли поток демоном.
"""
from functools import wraps
from threading import Thread, enumerate
import time


def run_in_thread(thread_name, is_daemon):
    def inner_run_in_thread(func):

        @wraps(func)
        def wrapper(*args):
            t = Thread(target=func, args=args, name=thread_name, daemon=is_daemon)
            t.start()
            return t
        return wrapper
    return inner_run_in_thread


@run_in_thread("Thread_name", False)
def between_markers(text: str, begin: str, end: str):
    start = text.find(begin) + len(begin) if begin in text else None
    stop = text.find(end) if end in text else None
    print(text[start:stop])
    time.sleep(2)  # for testing purpose


if __name__ == "__main__":
    between_markers('What is >apple<', '>', '<')
    between_markers("<head><title>My new site</title></head>", "<title>", "</title>")
    between_markers('No[/b] hi', '[b]', '[/b]')
    between_markers('No [b]hi', '[b]', '[/b]')
    between_markers('No hi', '[b]', '[/b]')
    between_markers('No <hi>', '>', '<')
    print(enumerate())    # for testing purpose









