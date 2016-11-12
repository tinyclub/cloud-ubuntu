#!/bin/bash

id -u ubuntu &>/dev/null || useradd --create-home --shell /bin/bash --user-group --groups adm,sudo ubuntu

[ -z "$UNIX_PWD" ] && UNIX_PWD=ubuntu

/bin/echo "ubuntu:$UNIX_PWD" | /usr/sbin/chpasswd

[ -z "$VNC_PWD" ] && VNC_PWD=ubuntu

[ ! -d /home/ubuntu/.vnc ] && sudo -u ubuntu mkdir -p /home/ubuntu/.vnc
sudo -u ubuntu /usr/bin/x11vnc -storepasswd $VNC_PWD  /home/ubuntu/.vnc/passwd

sudo -u ubuntu -i bash -c "cp -r /usr/share/desktop/.config /home/ubuntu/"

# /tmp
mount -t tmpfs none /tmp

/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

for f in /etc/startup.aux/*.sh
do
    . $f
done
