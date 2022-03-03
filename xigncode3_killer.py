from os import name
from re import T
from xml.etree.ElementTree import QName
import psutil


# def on_terminate(proc):
#     print("process {} terminated with exit code {}".format(proc, proc.returncode))


# procs = psutil.Process().children()
# for p in procs:
#     p.terminate()
# gone, alive = psutil.wait_procs(procs, timeout=3, callback=on_terminate)
# for p in alive:
#     p.kill()

import time


def get_client_process():
    while True:
        for p in psutil.process_iter(["pid", "name"]):
            print(p)
            if p.name == "LaTaleClient.exe":
                return p
        time.sleep(0.5)


proc = get_client_process()
while True:
    print(proc.children())
    time.sleep(5)
