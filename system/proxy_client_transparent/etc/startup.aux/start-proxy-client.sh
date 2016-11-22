#!/bin/bash
#
# start-proxy-client.sh -- config and start the proxy server with port and password
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../../

[ -z "$PROXY_SERVER" ] && \
    echo "Please run docker with ENV_ARGS='-e PROXY_SERVER=IP:PORT'" && exit 1
PROXY_SERVER="$(echo $PROXY_SERVER | tr ':' ' ')"

[ -z "$PROXY_PWD" ] && \
    echo "Please run docker with ENV_ARGS='-e PROXY_PWD=PASSWORD'" && exit 2

[ -z "$PROXY_PORT" ] && PROXY_PORT=1080

HPROXY_PASS=$PROXY_PWD ${TOP_DIR}/usr/local/bin/hev-socks5-client 127.0.0.1 $PROXY_PORT $PROXY_SERVER &

${TOP_DIR}/usr/local/bin/hev-socks5-tproxy 0.0.0.0 10800 0.0.0.0 5300 127.0.0.1 $PROXY_PORT &

sudo iptables-restore ${TOP_DIR}/etc/iptables/tproxy.rules
PROXY_SERVER_IP="$(echo $PROXY_SERVER | awk '{print $1}')"
PROXY_SERVER_PORT="$(echo $PROXY_SERVER | awk '{print $2}')"
sudo iptables -t nat -I OUTPUT -d $PROXY_SERVER_IP/32 -p tcp --dport $PROXY_SERVER_PORT -j RETURN

sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

gpasswd -d ubuntu adm
gpasswd -d ubuntu sudo
