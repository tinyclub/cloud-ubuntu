#!/bin/bash
#
# start-proxy-client.sh -- config and start the proxy server with port and password
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../..

[ -z "$PROXY_SERVER" ] && \
    echo "Please run docker with ENV_ARGS='-e PROXY_SERVER=IP:PORT'" && exit 1

[ -z "$PROXY_PWD" ] && \
    echo "Please run docker with ENV_ARGS='-e PROXY_PWD=PASSWORD'" && exit 2

[ -z "$PROXY_PORT" ] && PROXY_PORT=1080

PROXY_SERVER_IP=${PROXY_SERVER%:*}
PROXY_SERVER_PORT=${PROXY_SERVER#*:}

HPROXY_PASS=$PROXY_PWD ${TOP_DIR}/usr/local/bin/hev-socks5-client 127.0.0.1 $PROXY_PORT $PROXY_SERVER_IP $PROXY_SERVER_PORT &

${TOP_DIR}/usr/local/bin/hev-socks5-tproxy 0.0.0.0 10800 0.0.0.0 53 127.0.0.1 $PROXY_PORT &

sudo iptables-restore ${TOP_DIR}/etc/iptables/tproxy.rules
sudo iptables -t nat -I OUTPUT -d $PROXY_SERVER_IP/32 -p tcp --dport $PROXY_SERVER_PORT -j RETURN

sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

sudo gpasswd -d ubuntu adm
sudo gpasswd -d ubuntu sudo
