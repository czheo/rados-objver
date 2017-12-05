import boto
import boto.s3.connection
from boto.s3.key import Key
import os, sys
import json
import socket

dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

IF_VER = True

def connect():
    with open(os.path.join(dir_path, 'rgw.user')) as f:
        user_info = json.load(f)
        access_key = user_info['keys'][0]['access_key']
        secret_key = user_info['keys'][0]['secret_key']

        conn = boto.connect_s3(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            host = 'localhost',
            port = 7480,
            is_secure=False,               # uncomment if you are not using ssl
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
        return conn

conn = connect()
name = 'test_bucket'
existed = conn.lookup(name)
bucket = conn.get_bucket(name) if existed else None

def init_pool():
    global bucket
    if bucket:
        deleted = False
        while not deleted:
            try:
                conn.delete_bucket(name)
                deleted = True
            except:
                for ver in bucket.list_versions():
                    bucket.delete_key(ver.name, version_id = ver.version_id)
    bucket = conn.create_bucket(name)
    bucket.configure_versioning(IF_VER)
    bucket = conn.get_bucket(name)
    return bucket

def put(key, val):
    k = Key(bucket)
    k.key = key
    k.set_contents_from_string(val)

def get(key, ver=""):
    k = Key(bucket)
    k.key = key
    if ver:
        return k.get_contents_as_string(version_id = ver)
    else:
        return k.get_contents_as_string()

def ls():
    for obj in bucket.list():
        yield obj.key

def lsver():
    for obj in bucket.list_versions():
        yield (obj.key, obj.version_id)

init_pool()
