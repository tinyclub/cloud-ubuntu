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

echo -e "[Main]\nWorkers=4\nPort=${PROXY_PORT}\nListenAddress=0.0.0.0\n" >> \
	${TOP_DIR}/etc/hev-socks5-client.conf
echo -e "[Srv1]\nPort=${PROXY_SERVER_PORT}\nAddress=${PROXY_SERVER_IP}\nPassword=${PROXY_PWD}\n" >> \
	${TOP_DIR}/etc/hev-socks5-client.conf
echo -e "[Socks5]\nPort=${PROXY_PORT}\nAddress=127.0.0.1\n" >> \
	${TOP_DIR}/etc/hev-socks5-tproxy.conf

${TOP_DIR}/usr/local/bin/hev-socks5-client ${TOP_DIR}/etc/hev-socks5-client.conf &
${TOP_DIR}/usr/local/bin/hev-socks5-tproxy ${TOP_DIR}/etc/hev-socks5-tproxy.conf &

sudo iptables-restore ${TOP_DIR}/etc/iptables/tproxy.rules
sudo iptables -t nat -I OUTPUT -d $PROXY_SERVER_IP/32 -p tcp --dport $PROXY_SERVER_PORT -j RETURN

sudo bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

sudo gpasswd -d ubuntu adm
sudo gpasswd -d ubuntu sudo
