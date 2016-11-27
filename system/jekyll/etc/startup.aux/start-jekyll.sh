#!/bin/bash
#
# start-jekyll.sh -- start the jekyll service
#

[ -z "$JEKYLL_SRC" ] && JEKYLL_SRC=~/jekyll-bootstrap/
# For regular users, must bigger than 1024
[ -z "$JEKYLL_PORT" ] && JEKYLL_PORT=8080
[ -z "$JEKYLL_HOST" ] && JEKYLL_HOST=`ifconfig eth0 | grep "inet addr" | sed -e "s/ *inet addr:\([0-9\.]*\) .*/\1/g"`

[ -z "$UNIX_USER" ] && UNIX_USER=ubuntu

cd $JEKYLL_SRC
sudo -u $UNIX_USER /usr/local/bin/jekyll s -w --future --limit_posts 10 -s $JEKYLL_SRC -P $JEKYLL_PORT -H $JEKYLL_HOST
