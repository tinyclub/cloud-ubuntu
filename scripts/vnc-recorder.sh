#!/bin/bash

TOP_DIR=$(cd $(dirname $0) && pwd)/../

LAB_SECURITY=0 \
	VNC_MOUNT=1 VNC_RECORD=0 \
	GATEONE_PUBLIC=1 GATEONE_AUTH="none" \
	VNC_AUTH='' VNC_PUBLIC=1 LOCAL_VNC_PORT=6080 \
	UNIX_PWD=`pwgen -c -n -s -1 25` ENCRYPT_CMD=md5sum \
	${TOP_DIR}/scripts/web-ubuntu.sh
