#!/bin/bash
#
# proxy-server.sh -- launch the proxy server
#
# Usage:
#
#    PROXY_PWD=PASSWORD [PROXY_PORT=80] [ENCRYPT_CMD=md5sum] ./scripts/proxy-server.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$PROXY_PORT" ] && PROXY_PORT=80
# Available encrypt cmds: sha1sum, sha224sum, cksum, sha256sum, sha512sum, md5sum, sha384sum, sum
[ -z "$ENCRYPT_CMD" ] && ENCRYPT_CMD="cat"
[ -n "$PROXY_PWD" ] && PROXY_PWD=`echo -n $PROXY_PWD | $ENCRYPT_CMD | cut -d' ' -f1`
[ -n "$PROXY_PWD" ] && EXTRA_ARGS="$EXTRA_ARGS -e PROXY_PWD=$PROXY_PWD"

EXTRA_ARGS="$EXTRA_ARGS -e PROXY_PORT=$PROXY_PORT"

PORT_MAP="-p $PROXY_PORT:$PROXY_PORT" \
    HOST_NAME=localhost \
    EXTRA_ARGS="$EXTRA_ARGS --cpuset-cpus=0 --memory=96M" \
    ${TOP_DIR}/run proxy_server
