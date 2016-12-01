#!/bin/bash
#
# proxy-server.sh -- launch the proxy server
#
# Usage:
#
#    PROXY_PWD=PASSWORD [PROXY_PORT=80] ./scripts/proxy-server.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$PROXY_PORT" ] && PROXY_PORT=80
[ -n "$PROXY_PWD" ] && EXTRA_ARGS="$EXTRA_ARGS -e PROXY_PWD=$PROXY_PWD"

EXTRA_ARGS="$EXTRA_ARGS -e PROXY_PORT=$PROXY_PORT"

PORT_MAP="-p $PROXY_PORT:$PROXY_PORT" \
    HOST_NAME=localhost \
    EXTRA_ARGS="$EXTRA_ARGS --cpuset-cpus=0 --memory=96M" \
    ${TOP_DIR}/run proxy_server
