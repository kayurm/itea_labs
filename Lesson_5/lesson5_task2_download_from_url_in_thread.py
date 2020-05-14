""""
Kateryna Yurmanovych
     lesson 5
     Task 2
Создать функцию, которая будет скачивать файл из интернета по
ссылке, повесить на неё созданный декоратор. Создать список из 10
ссылок, по которым будет происходить скачивание. Создать список
потоков, отдельный поток, на каждую из ссылок. Каждый поток
должен сигнализировать, о том, что, он начал работу и по какой
ссылке он работает, так же должен сообщать когда скачивание
закончится."""

from functools import wraps
from threading import Thread
import requests


def run_in_thread(is_daemon):
    def inner_run_in_thread(func):
        @wraps(func)
        def wrapper(*args):
            t = Thread(target=func, args=args, daemon=is_daemon)
            t.start()
            return t
        return wrapper
    return inner_run_in_thread


@run_in_thread(is_daemon=False)
def download_file_by_url(url_in, file_name):
    print(f"Downloading from the url: {url_in} has started")
    r = requests.get(url_in)
    with open(file_name, 'wb') as f:
        f.write(r.content)
    print(f"Downloading from the url {url} has finished")


if __name__ == "__main__":
    url_list = [
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/MODERN/hckr_hnd.txt",
        "http://textfiles.com/etext/AUTHORS/SHAKESPEARE/shakespeare-macbeth-46.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt",
        "http://textfiles.com/etext/FICTION/alicewonder.txt"
    ]
    for index, url in enumerate(url_list):
        download_file_by_url(url, str(index + 1) + "_file")
