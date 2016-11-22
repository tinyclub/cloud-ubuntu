#!/bin/bash
#
# pwgen.sh -- set a password for proxy server
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../../

[ -z "$PROXY_PWD" ] && PROXY_PWD=`pwgen -c -n -s -1 15`
[ -z "$PROXY_DNS" ] && PROXY_DNS=8.8.8.8
[ -z "$PROXY_PORT" ] && PROXY_PORT=80

HPROXY_PASS=$PROXY_PWD ${TOP_DIR}/usr/local/bin/hev-socks5-proxy 0.0.0.0 $PROXY_PORT $PROXY_DNS
