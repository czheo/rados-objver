default: clean libcls_objver.so

libcls_objver.so:
	cd ../ceph/build/ && make cls_objver
	cp ../ceph/build/lib/libcls_objver.so .

clean:
	rm -fv libcls_objver.so ../ceph/build/lib/libcls_objver.so
