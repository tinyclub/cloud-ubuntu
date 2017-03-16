#!/bin/bash
#
# web-ubuntu.sh
#
# 1. Record the screen session into noVNC/recordings/
#
#    $ VNC_RECORD=1 ./scripts/web-ubuntu.sh
#
# 2. Playback
#
#    http://localhost:6080/tests/vnc_playback.html?data=vnc.record.data.1&mode=realtime
#    http://localhost:6080/play.html?data=vnc.record.data.1&mode=realtime
#
# 3. Public for 'vnc://host:port' access
#
#    VNC_PUBLIC=1 ./scripts/web-ubuntu.sh
#    GATEONE_PUBLIC=1 ./scripts/web-ubuntu.sh
#
# 4. Basic Http Auth (Chromium not support, Firefox works)
#
#    VNC_AUTH='user:pass' ./scripts/web-ubuntu.sh
#    GATEONE_AUTH='pam' ./scripts/web-ubuntu.sh    # options: none, pam, ...
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

source ${TOP_DIR}/config $* >/dev/null 2>&1

[ -z "$DEFAULT_PORT_MAP" ] \
    && DEFAULT_PORT_MAP=" -p $LOCAL_VNC_PORT:$VNC_PORT -p $LOCAL_SSH_PORT:$SSH_PORT -p $LOCAL_WEBSSH_PORT:$WEBSSH_PORT " \
    && echo "PORTS: VNC=$LOCAL_VNC_PORT SSH=$LOCAL_SSH_PORT WEBSSH=$LOCAL_WEBSSH_PORT"

# Available encrypt cmds: sha1sum, sha224sum, cksum, sha256sum, sha512sum, md5sum, sha384sum, sum
[ -z "$ENCRYPT_CMD" ] && ENCRYPT_CMD="cat"
[ -n "$UNIX_PWD" ] && UNIX_PWD=`echo -n $UNIX_PWD | $ENCRYPT_CMD | cut -d' ' -f1`
[ -n "$VNC_PWD" ] && VNC_PWD=`echo -n $VNC_PWD | $ENCRYPT_CMD | cut -d' ' -f1`
[ -z "$VNC_RECORD" ] && VNC_RECORD=0
[ -z "$VNC_MOUNT" ] && VNC_MOUNT=0
[ -z "$VNC_PLAYER" ] && VNC_PLAYER=0
[ -z "$VNC_TIMEOUT" ] && VNC_TIMEOUT=0
[ -z "$VNC_PUBLIC" ] && VNC_PUBLIC=0
[ -z "$VNC_AUTH" ] && VNC_AUTH=""
[ -z "$GATEONE_AUTH" ] && GATEONE_AUTH=""
[ -z "$GATEONE_PUBLIC" ] && GATEONE_PUBLIC=""

if [ $VNC_RECORD -eq 1 -o $VNC_PLAYER -eq 1 ]; then
    VNC_MOUNT=1
fi

if [ $VNC_MOUNT -eq 1 ]; then
    VNC_RECORD_DIR=/noVNC/recordings
    VNC_RECORD_FILE=$VNC_RECORD_DIR/vnc.record.data
    LOCAL_RECORD_DIR=$TOP_DIR/$VNC_RECORD_DIR
    [ ! -d $LOCAL_RECORD_DIR ] && mkdir -p $LOCAL_RECORD_DIR
    VOLUME_MAP=" -v $LOCAL_RECORD_DIR:$VNC_RECORD_DIR "
    echo "LOG: VNC screen recorded in $VNC_RECORD_FILE"
fi

EXTRA_ARGS="$EXTRA_ARGS -e PROXY_SPEED_LIMIT=0 -e NOSSL=$NOSSL"
EXTRA_ARGS="$EXTRA_ARGS -e VNC_RECORD=$VNC_RECORD -e VNC_PLAYER=$VNC_PLAYER -e VNC_TIMEOUT=$VNC_TIMEOUT -e VNC_RECORD_FILE=$VNC_RECORD_FILE $VOLUME_MAP"
EXTRA_ARGS="$EXTRA_ARGS -e VNC_PUBLIC=$VNC_PUBLIC -e VNC_AUTH=$VNC_AUTH -e GATEONE_AUTH=$GATEONE_AUTH -e GATEONE_PUBLIC=$GATEONE_PUBLIC"

EXTRA_ARGS="$EXTRA_ARGS" UNIX_PWD="$UNIX_PWD" VNC_PWD="$VNC_PWD" PORT_MAP="$DEFAULT_PORT_MAP" ${TOP_DIR}/run web
