#!/bin/bash
#
# proxy-client-transparent.sh -- launch the transparent proxy client
#
# Usage:
#
#    PROXY_SERVER=IP:PORT PROXY_PWD=PASSWORD PROXY_PORT=1080 [MAP_PORT=1] [ENCRYPT_CMD=md5sum] ./scripts/proxy-client-transparent.sh
#
# Note: To use this proxy in web browser of host, please set socks v5 proxy: localhost:1080, and enable "Remote DNS".
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$PROXY_PORT" ] && PROXY_PORT=1080
EXTRA_ARGS="$EXTRA_ARGS -e PROXY_PORT=$PROXY_PORT"

[ -n "$MAP_PORT" ] && EXTRA_ARGS="$EXTRA_ARGS -p $PROXY_PORT:$PROXY_PORT"

[ -n "$PROXY_LIMIT" ] && EXTRA_ARGS="$EXTRA_ARGS -e PROXY_LIMIT=$PROXY_LIMIT"

# Available encrypt cmds: sha1sum, sha224sum, cksum, sha256sum, sha512sum, md5sum, sha384sum, sum
[ -z "$ENCRYPT_CMD" ] && ENCRYPT_CMD="cat"
[ -n "$PROXY_PWD" ] && PROXY_PWD=`echo $PROXY_PWD | $ENCRYPT_CMD | cut -d' ' -f1`

EXTRA_ARGS="$EXTRA_ARGS --dns 127.0.0.1 -e PROXY_SERVER=$PROXY_SERVER -e PROXY_PWD=$PROXY_PWD" ${TOP_DIR}/run proxy_client_transparent
