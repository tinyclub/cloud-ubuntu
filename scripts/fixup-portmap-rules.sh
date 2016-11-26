#!/bin/bash
#
# fixup-portmap-rules.sh -- Fix up iptables rules for docker port mapping
#

# Generate from docker ps -a...
ports=`docker ps -a --format="{{.Ports}}" | tr ' ' '>' | tr ',' '\n' | sed -e "s%.*>\([0-9]*\)/.*%\1%g" | sort -g -u | uniq | tr '\n' ' '`
[ -z "$ports" ] && ports="1080 6080 443 22"

# Generate from --bip of dockerd
dnet=`ps -ef | grep dockerd | grep -v grep | sed -e "s%.*bip=\([0-9\.]*\)/.*%\1%g"`
[ -z "$dnet" ] && dnet=`ifconfig docker0 | grep "inet addr" | sed -e "s/ *inet addr:\([0-9\.]*\) .*/\1/g"`
[ -z "$dnet" ] && dnet=10.66.33.10
dnet=$(echo $dnet | cut -d'.' -f1-2)".0.0/16"

for port in $ports
do
    iptables -t nat -A POSTROUTING ! -s $dnet -d $dnet -p tcp -m tcp --dport $port -j MASQUERADE
done
