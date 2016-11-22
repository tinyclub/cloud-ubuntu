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

gpasswd -d ubuntu adm
gpasswd -d ubuntu sudo

${TOP_DIR}/usr/local/bin/hev-socks5-client 0.0.0.0 $PROXY_PORT $PROXY_PWD $PROXY_SERVER &
