#!/bin/bash
#
# proxy-relay.sh -- launch the proxy relay server
#
# Usage:
#
#    PROXY_SERVER=IP:PORT [RELAY_IP=HOST_IP] [RELAY_PORT=8080]" ./scripts/proxy-relay.sh
#
#    Note: The ip of RELAY_SERVER is often the ip address of ethX of this host
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$RELAY_PORT" ] && RELAY_PORT=8080

RELAY_SERVER=$RELAY_IP:$RELAY_PORT

PORT_MAP="-p $RELAY_PORT:$RELAY_PORT" \
    EXTRA_ARGS="$EXTRA_ARGS -e PROXY_SERVER=$PROXY_SERVER -e RELAY_SERVER=$RELAY_SERVER" ${TOP_DIR}/run proxy_relay
