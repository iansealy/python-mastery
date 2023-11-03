# follow.py
import os
import time


def follow(logfile):
    f = open(logfile)
    f.seek(0, os.SEEK_END)  # Move file pointer 0 bytes from end of file
    while True:
        line = f.readline()
        if line == "":
            time.sleep(0.1)  # Sleep briefly and retry
            continue
        yield line
