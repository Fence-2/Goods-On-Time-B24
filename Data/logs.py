from os import path, mkdir
from time import strftime, localtime

if not path.exists(r".\Logs"):
    mkdir(r".\Logs")

if not path.exists(r".\Logs\logs.txt"):
    with open(r".\Logs\logs.txt", "w", encoding="utf-8"):
        pass


def log(str_):
    with open(r".\Logs\logs.txt", "a", encoding="utf-8") as log_file:
        log_time = strftime("%m/%d/%Y, %H:%M:%S", localtime())
        log_file.write(f"[{log_time}] {str_}\n")

log("-----------------------Старт программы----------------------")