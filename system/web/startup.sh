#!/bin/bash

# /tmp
mount -t tmpfs none /tmp

for f in /etc/startup.aux/*.sh
do
    . $f
done

/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
