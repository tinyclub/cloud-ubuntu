#!/bin/bash
#
# proxy-server.sh -- launch the proxy server
#
# Usage:
#
#    ENV_ARGS="-e PROXY_PWD=PASSWORD" ./scripts/proxy-server.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

PORT_MAP="-p 80:80" HOST_NAME=localhost EXTRA_ARGS="--cpuset-cpus=0 --memory=96M" ${TOP_DIR}/run proxy_server
