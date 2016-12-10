#!/bin/bash

TOP_DIR=$(cd $(dirname $0) && pwd)/../

source ${TOP_DIR}/config $*

DEFAULT_PORT_MAP=" -p $LOCAL_VNC_PORT:$VNC_PORT -p $LOCAL_SSH_PORT:$SSH_PORT -p $LOCAL_WEBSSH_PORT:$WEBSSH_PORT "

PORT_MAP="$DEFAULT_PORT_MAP" ./run web
