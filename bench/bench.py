#! /usr/bin/env python
import os, sys
this_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(this_dir))

import client 
# import raw_client as client
# import rgw_client as client
from Queue import Queue
from threading import Thread
from time import time, sleep

def mean(lst):
    return sum(lst) / max(len(lst), 1)

op = sys.argv[1]
q = Queue()
print '# of threads\tthroughput\tlat avg\tmax\tmin'
load_dir = sys.argv[2]
NUM_OF_THREAD = int(sys.argv[3])
num_of_thread = 0
while num_of_thread < NUM_OF_THREAD:
    if op == 'put':
        sleep(1)
        client.init_pool()
        sleep(1)
    
    times = []
    # consumer
    if op == 'put':
        def worker():
            while True:
                path, vers= q.get()
                # real work
                for ver in vers:
                    f = os.path.join(path, ver)
                    # print i, f
                    start = time()
                    client.put(path, f)
                    duration = time() - start
                    times.append(duration)
                q.task_done()
    elif op == 'get':
        def worker():
            while True:
                obj = q.get()
                # real work
                start = time()
                client.get(obj)
                duration = time() - start
                times.append(duration)
                q.task_done()
    elif op == 'getver':
        def worker():
            while True:
                obj, ver = q.get()
                # real work
                start = time()
                client.get(obj, ver=ver)
                duration = time() - start
                times.append(duration)
                q.task_done()

    t = Thread(target=worker)
    t.daemon = True
    num_of_thread += 1
    t.start()

    start = time()
    # producer
    if op == 'put':
        for path, subdirs, files in os.walk(load_dir):
            if files:
                q.put((path, sorted(files, key=int)))
    elif op == 'get':
        # for i in range(1):
        for i in range(10):
            for obj in client.ls():
                q.put(obj)
    elif op == 'getver':
        # for obj, ver in client.lsver():
        for obj in client.ls():
            for ver in client.lsver(obj):
                q.put((obj, ver))

    q.join()
    total = time() - start

    print '%d\t%f\t%f\t%f\t%f\t' % (num_of_thread, len(times) / total, mean(times), max(times), min(times))
