#! /usr/bin/env python
import subprocess
import client
import heapq

def sh(s):
    return subprocess.check_output(s, shell=True)

files = sh('sudo rados -p test ls').split()

res = []
for i, f in enumerate(files):
    vers = client.lsver(f).split()
    print '%d/%d' % (i+1, len(files)), f, len(vers)
    res.append(
        (f, len(vers))
    )

res.sort(key=lambda x: -x[1])

for f in res[:10]:
    print f
