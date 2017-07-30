import os
import time
import shutil

while True:
    for i in os.scandir("live"):
        if i.name[0] != '.' and i.is_dir() and time.time() - i.stat().st_mtime > 43200:
            shutil.rmtree("live/" + i.name)
