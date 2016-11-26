#!/bin/bash
#
# start-tproxy-client.sh -- replace the route with the transparent proxy ip
#

DEFAULT_GW=$(route -n | grep "^0.0.0.0" | tr -s ' ' | cut -d' ' -f2)

if [ -z "$TPROXY_IP" ]; then
    echo "Warning: Please run docker with ENV_ARGS='-e TPROXY_IP=IP'"
    TPROXY_IP=$(echo $DEFAULT_GW | cut -d'.' -f1-3)".1"
fi

echo "LOG: Change the default gateway from $DEFAULT_GW to $TPROXY_IP"

sudo route del default gw $DEFAULT_GW eth0
sudo route add default gw $TPROXY_IP eth0
