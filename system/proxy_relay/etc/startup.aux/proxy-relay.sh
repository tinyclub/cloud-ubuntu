#!/bin/bash
#
# proxy-relay.sh -- launch the proxy relay server
#
# Usage:
#
#    PROXY_SERVER=IP:PORT RELAY_SERVER=IP:PORT ./scripts/proxy-relay.sh
#
#    Note: The ip of RELAY_SERVER is often the ip address of ethX of this host
#
# ref: http://www.systutorials.com/816/port-forwarding-using-iptables/
#

[ -z "$PROXY_SERVER" ] && \
    echo "Please pass PROXY_SERVER with IP:PORT'" && exit 1
[ -z "$RELAY_SERVER" ] && \
    echo "Please pass RELAY_SERVER with IP:PORT'" && exit 1

proxy_tunnel_rules=`mktemp`

SERVER_IP=${PROXY_SERVER%:*}
SERVER_PORT=${PROXY_SERVER#*:}
RELAY_IP=${RELAY_SERVER%:*}
RELAY_PORT=${RELAY_SERVER#*:}

[ -z "$RELAY_IP" ] && RELAY_IP=`ip addr show eth0 | grep "inet " | sed -e "s%.*inet \([0-9.]*\).*%\1%g"`

echo "PROXY_SERVER: $SERVER_IP:$SERVER_PORT"
echo "RELAY_SERVER: $RELAY_IP:$RELAY_PORT"

cat <<EOF | tee $proxy_tunnel_rules
# ========= RELAY RULES START =========
*filter
-A FORWARD -i eth0 -j ACCEPT
-A FORWARD -i eth1 -j ACCEPT
COMMIT
*nat
-A PREROUTING -d $RELAY_IP/32 -p tcp -m tcp --dport $RELAY_PORT -j DNAT --to-destination $SERVER_IP:$SERVER_PORT
-A POSTROUTING -d $SERVER_IP/32 -p tcp -m tcp --dport $SERVER_PORT -j SNAT --to-source $RELAY_IP
COMMIT
# ========= RELAY RULES END =========
EOF

sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
sudo iptables-restore -v $proxy_tunnel_rules
sudo iptables-save
sudo rm $proxy_tunnel_rules

which docker && sudo service docker restart
