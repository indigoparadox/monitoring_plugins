#!/bin/sh

echo "<<<mk_gluster_peers>>>"

gluster peer status | sed ':a;N;$!ba;s/\(\S\)\n/\1|/g'

echo "<<<mk_gluster_volumes>>>"

gluster volume info | sed ':a;N;$!ba;s/\(\S\)\n/\1|/g'

