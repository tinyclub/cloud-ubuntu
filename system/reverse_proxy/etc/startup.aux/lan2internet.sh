#!/bin/bash
#
# lan2internet.sh -- Bind a port of local to a port of internet, allow to access lan from internet
#

[ -z "$SSH_SERVER" -o -z "$SSH_PASS" ] && echo "LOG: SSH_SERVER and SSH_PASS can not be empty" && exit 0
[ -z "$SSH_PORT" ] && SSH_PORT=2222
[ -z "$SSH_USER" ] && SSH_USER=ubuntu

[ -z "$LOCAL_ADDR" ] && LOCAL_ADDR=localhost
[ -z "$LOCAL_SSH_PORT" ] && LOCAL_SSH_PORT=22
[ -z "$LOCAL_VNC_PORT" ] && LOCAL_VNC_PORT=5900
[ -z "$REMOTE_SSH_PORT" ] && REMOTE_SSH_PORT=2001
[ -z "$REMOTE_VNC_PORT" ] && REMOTE_VNC_PORT=5001

CMD_PRE="SSHPASS=$SSH_PASS sshpass -e ssh -nNT -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no $SSH_USER@$SSH_SERVER -p $SSH_PORT -R"

SSH_CMD="$CMD_PRE $REMOTE_SSH_PORT:$LOCAL_ADDR:$LOCAL_SSH_PORT"
VNC_CMD="$CMD_PRE $REMOTE_VNC_PORT:$LOCAL_ADDR:$LOCAL_VNC_PORT"
[ -n "$REMOTE_PORT" -a -n "$LOCAL_PORT" ] && MISC_CMD="$CMD_PRE $REMOTE_PORT:$LOCAL_ADDR:$LOCAL_PORT"

eval $SSH_CMD &
eval $VNC_CMD &
[ -n "$MISC_CMD" ] && eval $MISC_CMD &
