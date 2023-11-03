# follow.py
import os
import time


def follow(filename):
    try:
        with open(filename, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line == "":
                    time.sleep(0.1)  # Sleep briefly to avoid busy wait
                    continue
                yield line
    except GeneratorExit:
        print("Following Done")
