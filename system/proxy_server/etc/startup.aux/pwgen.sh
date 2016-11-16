#!/bin/bash
#
# pwgen.sh -- set a password for proxy server
#

[ -z "$PROXY_PWD" ] && PROXY_PWD=`pwgen -c -n -s -1 15`

echo "PROXY_PWD: $PROXY_PWD"

sed -i -e "s%PROXY_PWD%$PROXY_PWD%g" /etc/supervisor/supervisord.conf
