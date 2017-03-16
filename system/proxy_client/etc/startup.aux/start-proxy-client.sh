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

sudo gpasswd -d ubuntu adm
sudo gpasswd -d ubuntu sudo

PROXY_SERVER_IP=${PROXY_SERVER%:*}
PROXY_SERVER_PORT=${PROXY_SERVER#*:}

echo -e "[Main]\nWorkers=4\nPort=${PROXY_PORT}\nListenAddress=0.0.0.0\n" >> \
	${TOP_DIR}/etc/hev-socks5-client.conf
echo -e "[Srv1]\nPort=${PROXY_SERVER_PORT}\nAddress=${PROXY_SERVER_IP}\nPassword=${PROXY_PWD}\n" >> \
	${TOP_DIR}/etc/hev-socks5-client.conf

${TOP_DIR}/usr/local/bin/hev-socks5-client ${TOP_DIR}/etc/hev-socks5-client.conf
