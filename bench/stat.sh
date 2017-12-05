#!/bin/bash

pool='test'
list=`rados -p $pool ls`

(
for obj in $list; do
  # echo -en "$obj ";
  rados -p $pool listomapvals $obj | awk -e '
    /^value \(.* bytes\)/ { sizevalue += substr($2, 2, length($2))}
    END { print(sizevalue) }
  '
done
) | awk '{s+=$1} END {print s}'
