#!/bin/bash
#
# start-proxy-server.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../..

[ -z "$PROXY_PWD" ] && PROXY_PWD=`pwgen -c -n -s -1 15`
[ -z "$PROXY_DNS" ] && PROXY_DNS=8.8.8.8
[ -z "$PROXY_PORT" ] && PROXY_PORT=80

echo "PROXY_PWD: $PROXY_PWD"

echo -e "[Main]\nWorkers=4\nPort=${PROXY_PORT}\nListenAddress=0.0.0.0\nDNSAddress=${PROXY_DNS}\n" >> \
	${TOP_DIR}/etc/hev-socks5-server.conf
echo -e "[Auth]\nPassword=${PROXY_PWD}\n" >> \
	${TOP_DIR}/etc/hev-socks5-server.conf

${TOP_DIR}/usr/local/bin/hev-socks5-server ${TOP_DIR}/etc/hev-socks5-server.conf
