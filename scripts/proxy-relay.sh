#!/bin/bash
#
# proxy-relay.sh -- launch the proxy relay server
#
# Usage:
#
#    PORT_MAP="-p 8080:8080" ENV_VARS="-e PROXY_SERVER=IP:PORT -e RELAY_SERVER=:PORT" ./scripts/proxy-relay.sh
#
#    Note: The ip of RELAY_SERVER is often the ip address of ethX of this host
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

${TOP_DIR}/run proxy_relay
