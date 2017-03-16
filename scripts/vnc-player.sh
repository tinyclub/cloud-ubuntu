#!/bin/bash

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$LOCAL_VNC_PORT" ] && LOCAL_VNC_PORT=6081

source ${TOP_DIR}/config $* >/dev/null 2>&1

UNIX_PWD=`pwgen -c -n -s -1 25` ENCRYPT_CMD=md5sum LAB_SECURITY=0 VNC_PLAYER=1 DEFAULT_PORT_MAP="-p $LOCAL_VNC_PORT:$VNC_PORT" \
    ${TOP_DIR}/scripts/web-ubuntu.sh
