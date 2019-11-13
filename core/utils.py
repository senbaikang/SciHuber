import functools
import inspect
import os


def caller_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(inspect.stack()[1].function)
    return wrapper


def check_and_initialize_folder(path):
    directory_name = "resources"
    # doc_links = "doc_links.json"
    # failed_doc_links = "failed_doc_links.txt"
    # captcha_codes = "captcha_codes.json"
    # scihub_links = "scihub_links.txt"

    if not os.path.isdir(path + '/' + directory_name):
        os.mkdir(path + '/' + directory_name)

