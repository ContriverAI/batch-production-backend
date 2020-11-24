import os
from datetime import datetime, timedelta
import freeport
import time
import threading
import signal
import subprocess

def a():
    os.system("python3 api.py")

next_date = datetime.now() + timedelta(seconds=10)
x = threading.Thread(target=a)
x.start()

while(True):
    cur_date = datetime.now()
    if next_date < cur_date:
        command = "netstat -lpn | grep :9001"
        c = subprocess.Popen(command, shell=True)
        # print(c)
        # pid = int(stdout.decode().strip().split(' ')[-1])
        # os.kill(pid, signal.SIGTERM)
        # x.start()
        # next_date = cur_date + timedelta(seconds=10)
    else:
        pass
