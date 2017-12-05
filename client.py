#! /usr/bin/env python

import rados
import json
import argparse
import os, sys

# init ceph
CONFFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_cluster/ceph.conf")
KEYFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_cluster/ceph.client.admin.keyring")
POOL = "test"

cluster = rados.Rados(conffile=CONFFILE, conf={"keyring": KEYFILE})
cluster.connect()
ioctx = cluster.open_ioctx(POOL)

def init_pool():
    os.system("sudo rados purge test --yes-i-really-really-mean-it > /dev/null")

def get(name, ver = ""):
    ret, out = ioctx.execute(name, 'objver', 'get', ver, length=2**16)
    if ret < 0:
        raise Exception
    return out

def put(name, path):
    with open(path) as f:
        return ioctx.execute(name, 'objver', 'put', f.read())

def lsver(name):
    """list version"""
    ret, out = ioctx.execute(name, 'objver', 'lsver', "")
    if ret < 0:
        raise Exception
    return out.split()

def ls():
    # it = ioctx.list_objects()
    return [x.key for x in ioctx.list_objects()]

def main(args):
    if args.command == "get":
        print(get(args.name, args.ver)),
    elif args.command == "put":
        print(put(args.name, args.path)),
    elif args.command == "lsver":
        for ver in lsver(args.name):
            print ver
    elif args.command == 'ls':
        for obj in ls():
            print(obj)

if __name__ == "__main__":
    # arg parse
    parser = argparse.ArgumentParser(prog='objver',
             description='Rados object versioning')

    subparsers = parser.add_subparsers(dest='command')

    # get
    parser_get = subparsers.add_parser('get', help='get')
    parser_get.add_argument('name')
    parser_get.add_argument('--ver', default="")

    # put
    parser_put = subparsers.add_parser('put', help='put')
    parser_put.add_argument('name')
    parser_put.add_argument('path')

    # lsver
    parser_lsver = subparsers.add_parser('lsver', help='list versions')
    parser_lsver.add_argument('name')

    # ls
    parser_lsver = subparsers.add_parser('ls', help='list objects')

    args = parser.parse_args()
    if args.command:
        main(args)
    else:
        parser.print_help()
