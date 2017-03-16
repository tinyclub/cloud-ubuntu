#!/bin/bash
#
# vnc-playback.sh
#
# To playback the VNC session, must record it with:
#
#    $ VNC_RECORD=1 ./scripts/web-ubuntu.sh
#
# The VNC data is stored in noVNC/recordings/ and named with vnc.record.data.[session number]
#
# Play back the session:
#
#    $ VNC_DATA=vnc.record.data.1 ./scripts/vnc-playback.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/..

source ${TOP_DIR}/config $*

[ -z "$ENCRYPT_CMD" ] && ENCRYPT_CMD=md5sum
[ -z "$CONTAINER_IP" ] && CONTAINER_IP=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' $CONTAINER_NAME`
[ -z "$PORT" ] && PORT=$LOCAL_VNC_PORT

[ -n "$1" ] && VNC_DATA=$1
[ -z "$VNC_DATA" ] && VNC_DATA=vnc.record.data.1

if [ "$VNC_PORT" != "6080" ]; then
    token=`echo -n $VNC_PORT | $ENCRYPT_CMD | cut -d' ' -f1`
else
    token=`echo -n $CONTAINER_IP | $ENCRYPT_CMD | cut -d' ' -f1`
fi

URL="$HTTP://$HOST_NAME:$PORT/play.html?data=$VNC_DATA"

echo "LOG: URL: $URL"

(chromium-browser $URL >/dev/null 2>&1 &) >/dev/null 2>&1
