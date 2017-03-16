#!/bin/bash
#
# vnc-play.sh
#
# Start the vnc player (service):
#
#    $ ./scripts/vnc-player.sh
#
# Put the recorded sessions, e.g. vnc.record.data.1 in noVNC/recordings/
#
# Play the session:
#
#    $ VNC_DATA=vnc.record.data.1 ./scripts/vnc-play.sh
#

TOP_DIR=$(cd $(dirname $0) && pwd)/..

[ -z "$LOCAL_VNC_PORT" ] && LOCAL_VNC_PORT=6081

source ${TOP_DIR}/config $* >/dev/null 2>&1

LOCAL_VNC_PORT=$LOCAL_VNC_PORT ${TOP_DIR}/scripts/vnc-playback.sh $*
