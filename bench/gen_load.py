#! /usr/bin/env python
MAX_COMMIT = 10000

import mimetypes
import os, sys
from collections import Counter
from shutil import copyfile
this_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(this_dir))

import subprocess
import client

def sh(s):
    return subprocess.check_output(s, shell=True)

def valid_name(file_name):
    tp = mimetypes.guess_type(file_name)[0]
    if not tp:
        return False
    return "!" not in file_name and "@" not in file_name and os.path.isfile(file_name) and tp.startswith('text')

target_dir = sys.argv[1].rstrip('/')


if not os.path.exists(target_dir):
    exit("%s is not a dir" % target_dir)

load_dir = "%s_load" % os.path.basename(target_dir)
if os.path.exists(load_dir):
    sh("rm -rf %s" % load_dir)

sh("mkdir %s" % load_dir)

os.chdir(target_dir)
print "change dir:", os.getcwd()

# check out master
sh("git checkout master")

# get hash list
hash_lst = sh("git log --reverse --pretty=format:%H").split()
prev_hash = None
cnter = Counter()

count = 0

def mvfile(name, ver):
    to_dir = os.path.join(this_dir, load_dir, name)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    copyfile(name, os.path.join(to_dir, str(ver)))

    
for hash_val in hash_lst:
    count += 1
    print count, '/', len(hash_lst)
    if count > MAX_COMMIT:
        break
    if not prev_hash:
        # first commit
        print "check out", hash_val
        sh("git checkout %s" % hash_val)
        files = sh("git ls-files").split()
        for f in files:
            if valid_name(f):
                mvfile(f, cnter[f])
                cnter[f] += 1

    else:
        print "check out", hash_val
        sh("git checkout %s" % hash_val)
        files = sh("git diff --name-only %s %s" % (prev_hash, hash_val)).split()
        for f in files:
            if valid_name(f):
                mvfile(f, cnter[f])
                cnter[f] += 1

    prev_hash = hash_val
