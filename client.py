import rados
from os.path import expanduser
import json
import argparse

# init ceph
CONFFILE = expanduser("~/my_cluster/ceph.conf")
KEYFILE = expanduser("~/my_cluster/ceph.client.admin.keyring")
POOL = "test"

cluster = rados.Rados(conffile=CONFFILE, conf={"keyring": KEYFILE})
cluster.connect()
ioctx = cluster.open_ioctx(POOL)
# ret, data = ioctx.execute('oid', 'sdk', 'test_coverage_write', "test")

def get(name):
    return ioctx.execute(name, 'objver', 'get', "")

def put(name, path):
    with open(path) as f:
        return ioctx.execute(name, 'objver', 'put', f.read())

def lsver(name):
    return ioctx.execute(name, 'objver', 'lsver', "")

def main(args):
    if args.command == "get":
        print(get(args.name))
    elif args.command == "put":
        print(put(args.name, args.path))
    elif args.command == "lsver":
        print(lsver(args.name))

if __name__ == "__main__":
    # arg parse
    parser = argparse.ArgumentParser(prog='objver',
             description='Rados object versioning')

    subparsers = parser.add_subparsers(dest='command')

    # get
    parser_get = subparsers.add_parser('get', help='get')
    parser_get.add_argument('name')

    # put
    parser_put = subparsers.add_parser('put', help='put')
    parser_put.add_argument('name')
    parser_put.add_argument('path')

    # lsver
    parser_lsver = subparsers.add_parser('lsver', help='list versions')
    parser_lsver.add_argument('name')

    args = parser.parse_args()
    if args.command:
        main(args)
    else:
        parser.print_help()
