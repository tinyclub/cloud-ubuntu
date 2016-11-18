#!/bin/bash
#
# pwgen.sh -- set a password for proxy server
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../../

[ -z "$PROXY_PWD" ] && PROXY_PWD=`pwgen -c -n -s -1 15`

echo "PROXY_PWD: $PROXY_PWD"

sed -i -e "s%PROXY_PWD%$PROXY_PWD%g" ${TOP_DIR}/etc/supervisor/supervisord.conf
