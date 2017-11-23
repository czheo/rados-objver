ceph-deploy purge node-{0..3}
ceph-deploy purgedata node-{0..3}
ceph-deploy forgetkeys
rm ceph.*

ceph-deploy new node-0
cp _ceph.conf ceph.conf
ceph-deploy install --release kraken node-{0..3}
ceph-deploy mon create-initial

ceph-deploy admin node-{0..3}
ssh node-1 sudo rm -rf /var/local/osd0/*
ssh node-2 sudo rm -rf /var/local/osd1/*
ssh node-3 sudo rm -rf /var/local/osd2/*
ceph-deploy osd prepare node-1:/var/local/osd0
ceph-deploy osd prepare node-2:/var/local/osd1
ceph-deploy osd prepare node-3:/var/local/osd2
ssh node-1 sudo chown -R ceph /var/local/osd0
ssh node-2 sudo chown -R ceph /var/local/osd1
ssh node-3 sudo chown -R ceph /var/local/osd2
ceph-deploy osd activate node-1:/var/local/osd0
ceph-deploy osd activate node-2:/var/local/osd1
ceph-deploy osd activate node-3:/var/local/osd2
