#! /usr/bin/env python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import client

def sh(s):
    return subprocess.check_output(s, shell=True)

def valid_name(file_name):
    return "!" not in file_name and "@" not in file_name and os.path.isfile(file_name)

target_dir = sys.argv[1]

if not os.path.exists(target_dir):
    exit("%s is not a dir" % target_dir)

os.chdir(target_dir)
print "change dir:", os.getcwd()

# check out master
sh("git checkout master")

# get hash list
hash_lst = sh("git log --reverse --pretty=format:%H").split()
prev_hash = None

count = 0
for hash_val in hash_lst:
    if not prev_hash:
        # first commit
        print "check out", hash_val
        sh("git checkout %s" % hash_val)
        files = sh("git ls-files").split()
        for f in files:
            if valid_name(f):
                print "put", f
                print client.put(f, f)
    else:
        print "check out", hash_val
        sh("git checkout %s" % hash_val)
        files = sh("git diff --name-only %s %s" % (prev_hash, hash_val)).split()
        for f in files:
            if valid_name(f):
                print "put", f
                print client.put(f, f)

    prev_hash = hash_val
