#!/bin/bash
#
# reverse-proxy.sh -- run the reverse proxy container to allow some local ports be accessible from internet
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$SSH_SERVER" -o -z "$SSH_PASS" ] && echo "LOG: SSH_SERVER and SSH_PASS can not be empty" && exit 0
[ -z "$SSH_PORT" ] && SSH_PORT=2222
[ -z "$SSH_USER" ] && SSH_USER=ubuntu

[ -z "$BATCH" ] && BATCH=0
[ -z "$LOCAL_ADDR" ] && LOCAL_ADDR=localhost
[ -z "$LOCAL_SSH_PORT" ] && LOCAL_SSH_PORT=22
[ -z "$LOCAL_VNC_PORT" ] && LOCAL_VNC_PORT=5900
[ -z "$REMOTE_SSH_PORT" ] && REMOTE_SSH_PORT=2000
[ -z "$REMOTE_VNC_PORT" ] && REMOTE_VNC_PORT=5000

EXTRA_ARGS="-e SSH_SERVER=$SSH_SERVER -e SSH_PASS=$SSH_PASS -e LOCAL_ADDR=$LOCAL_ADDR -e REMOTE_SSH_PORT=$REMOTE_SSH_PORT -e REMOTE_VNC_PORT=$REMOTE_VNC_PORT -e BATCH=$BATCH" \
   ${TOP_DIR}/run reverse_proxy

# Note: The above for containers, the following for local system
#
# Example:
#         $ SSH_SERVER=a.b.c.d SSH_PASS=yyy ${TOP_DIR}/system/reverse_proxy/etc/startup.aux/lan2internet.sh
