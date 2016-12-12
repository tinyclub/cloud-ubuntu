#!/bin/bash
#
# lan2internet.sh -- Bind a port of local to a port of internet, allow to access lan from internet
#

[ -z "$SSH_SERVER" -o -z "$SSH_PASS" ] && echo "LOG: SSH_SERVER and SSH_PASS can not be empty" && exit 0
[ -z "$SSH_PORT" ] && SSH_PORT=2222
[ -z "$SSH_USER" ] && SSH_USER=ubuntu

[ -z "$BATCH" ] && BATCH=0

[ -z "$LOCAL_SSH_PORT" ] && LOCAL_SSH_PORT=22
[ -z "$LOCAL_VNC_PORT" ] && LOCAL_VNC_PORT=5900
[ -z "$REMOTE_SSH_PORT" ] && REMOTE_SSH_PORT=2000
[ -z "$REMOTE_VNC_PORT" ] && REMOTE_VNC_PORT=5000

CMD_PRE="SSHPASS=$SSH_PASS sshpass -e ssh -nNT -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no $SSH_USER@$SSH_SERVER -p $SSH_PORT -R"

if [ $BATCH -ne 0 ]; then
    [ -z "$LOCAL_ADDR" -o "$LOCAL_ADDR"=="localhost" ] && LOCAL_ADDR=10.66.33.1
    LOCAL_ADDR_BASE=${LOCAL_ADDR%.*}
else
    [ -z "$LOCAL_ADDR" ] && LOCAL_ADDR=localhost
fi

for ((i=0; i<=$BATCH; i++))
do
    ((REMOTE_SSH_PORT+=1))
    ((REMOTE_VNC_PORT+=1))
    [ $LOCAL_ADDR != "localhost" -a -n "$LOCAL_ADDR_BASE" ] && LOCAL_ADDR=${LOCAL_ADDR_BASE}.$((i+1))

    SSH_CMD="$CMD_PRE $REMOTE_SSH_PORT:$LOCAL_ADDR:$LOCAL_SSH_PORT"
    VNC_CMD="$CMD_PRE $REMOTE_VNC_PORT:$LOCAL_ADDR:$LOCAL_VNC_PORT"
    [ -n "$REMOTE_PORT" -a -n "$LOCAL_PORT" ] && MISC_CMD="$CMD_PRE $REMOTE_PORT:$LOCAL_ADDR:$LOCAL_PORT"

    eval $SSH_CMD &
    eval $VNC_CMD &
    [ -n "$MISC_CMD" ] && eval $MISC_CMD &
done
