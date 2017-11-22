#!/bin/bash

restart_node() {
  host=$1
  echo "restarting $host"
  scp libcls_objver.so $host:~
  ssh $host sudo rm /usr/lib/rados-classes/libcls_objver.so*
  ssh $host sudo mv libcls_objver.so /usr/lib/rados-classes/libcls_objver.so
  ssh $host sudo chown root /usr/lib/rados-classes/libcls_objver.so
  ssh $host sudo chgrp root /usr/lib/rados-classes/libcls_objver.so
  ssh $host sudo systemctl restart ceph.target
}

restart_node node-0
restart_node node-1
restart_node node-2
restart_node node-3

sleep 3

sudo ceph -s
