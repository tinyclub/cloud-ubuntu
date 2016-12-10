#!/bin/bash
#
# generate-vnc-tokens.sh -- Generate the "token: vnc-ip:vnc-port" map file
#
#   TODO: Use vnc-ip:vnc-port directly?
#
# By default, generate the token via md5sum the 'ip:port' string.
#

[ -z "$DEFAULT_GW" ] && DEFAULT_GW=$(route -n | grep "^0.0.0.0" | tr -s ' ' | cut -d' ' -f2)
[ -z "$ENCRYPT_CMD" ] && ENCRYPT_CMD=md5sum

port=5900
map=/vnc-tokens.txt
net=$(echo $DEFAULT_GW | cut -d'.' -f1-3)

for i in `seq 1 255`; do
    ip=$net.$i
    #token=$i; echo "$token: $ip_port"
    token=$(echo -n $ip | $ENCRYPT_CMD | cut -d' ' -f1); echo "$token: $ip:$port"
done | tee $map
