#!/bin/bash

TOP_DIR=$(cd $(dirname $0) && pwd)/../

source ${TOP_DIR}/config $* 2>&1 >/dev/null

DEFAULT_PORT_MAP=" -p $LOCAL_VNC_PORT:$VNC_PORT -p $LOCAL_SSH_PORT:$SSH_PORT -p $LOCAL_WEBSSH_PORT:$WEBSSH_PORT "

# Available encrypt cmds: sha1sum, sha224sum, cksum, sha256sum, sha512sum, md5sum, sha384sum, sum
[ -z "$ENCRYPT_CMD" ] && ENCRYPT_CMD="cat"
[ -n "$UNIX_PWD" ] && PROXY_PWD=`echo -n $UNIX_PWD | $ENCRYPT_CMD | cut -d' ' -f1`
[ -n "$VNC_PWD" ] && PROXY_PWD=`echo -n $VNC_PWD | $ENCRYPT_CMD | cut -d' ' -f1`

echo "PORTS: VNC=$LOCAL_VNC_PORT SSH=$LOCAL_SSH_PORT WEBSSH=$LOCAL_WEBSSH_PORT"
UNIX_PWD="$UNIX_PWD" VNC_PWD="$VNC_PWD" PORT_MAP="$DEFAULT_PORT_MAP" ./run web
