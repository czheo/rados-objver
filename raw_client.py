import rados
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
    return ioctx.read(name)

def put(name, path):
    with open(path) as f:
        return ioctx.write_full(name, f.read())

def ls():
    for obj in ioctx.list_objects():
        yield obj.key
