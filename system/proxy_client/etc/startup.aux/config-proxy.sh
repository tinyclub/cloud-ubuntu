#!/bin/bash
#
# config-proxy.sh -- config the proxy server, port and password
#

[ -z "$PROXY_SERVER" ] && \
    echo "Please run docker with ENV_VARS='-e PROXY_SERVER=IP:PORT'" && exit 1
PROXY_SERVER="$(echo $PROXY_SERVER | tr ':' ' ')"

[ -z "$PROXY_PWD" ] && \
    echo "Please run docker with ENV_VARS='-e PROXY_PWD=PASSWORD'" && exit 2

[ -z "$PROXY_PORT" ] && PROXY_PORT=1080

sed -i -e "s%PROXY_PWD%$PROXY_PWD%g;s%PROXY_PORT%$PROXY_PORT%g;s%PROXY_SERVER%$PROXY_SERVER%g" \
	/usr/local/bin/proxy-client.sh

chmod 700 /usr/local/bin/proxy-client.sh
gpasswd -d ubuntu adm
gpasswd -d ubuntu sudo
