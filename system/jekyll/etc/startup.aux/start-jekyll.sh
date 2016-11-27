#!/bin/bash
#
# start-jekyll.sh -- start the jekyll service
#

[ -z "$JEKYLL_SRC" ] && JEKYLL_SRC=~/jekyll-bootstrap/
[ -z "$JEKYLL_PORT" ] && JEKYLL_PORT=80
[ -z "$JEKYLL_HOST" ] && JEKYLL_HOST=`ifconfig eth0 | grep "inet addr" | sed -e "s/ *inet addr:\([0-9\.]*\) .*/\1/g"`

/usr/local/bin/jekyll s -w --future --limit_posts 10 -s $JEKYLL_SRC -P $JEKYLL_PORT -H $JEKYLL_HOST
