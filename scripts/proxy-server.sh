#!/bin/bash
#
# proxy-server.sh -- launch the proxy server
#
# Usage:
#
#    EXTRA_ARGS="-e PROXY_PWD=PASSWORD" ./scripts/proxy-server.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$PORT_MAP" ] && PORT_MAP="-p 80:80"

PORT_MAP="$PORT_MAP" HOST_NAME=localhost EXTRA_ARGS="$EXTRA_ARGS --cpuset-cpus=0 --memory=96M" ${TOP_DIR}/run proxy_server
