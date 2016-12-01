#!/bin/bash
#
# proxy-server.sh -- launch the proxy server
#
# Usage:
#
#    EXTRA_ARGS="-e PROXY_PWD=PASSWORD" ./scripts/proxy-server.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$PROXY_PORT" ] && PROXY_PORT=80

PORT_MAP="-p $PROXY_PORT:$PROXY_PORT" HOST_NAME=localhost EXTRA_ARGS="$EXTRA_ARGS --cpuset-cpus=0 --memory=96M -e PROXY_PORT=$PROXY_PORT" ${TOP_DIR}/run proxy_server
