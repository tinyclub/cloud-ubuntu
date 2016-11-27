#!/bin/bash
#
# jekyll.sh -- start the jekyll container
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

JEKYLL_GIT=https://github.com/plusjade/jekyll-bootstrap/
JEKYLL_LOCAL=${TOP_DIR}/jekyll-bootstrap/
JEKYLL_SRC=/home/ubuntu/jekyll-bootstrap/
JEKYLL_PORT=8080
JEKYLL_HOST=`ifconfig eth0 | grep "inet addr" | sed -e "s/ *inet addr:\([0-9\.]*\) .*/\1/g"`

[ ! -d $JEKYLL_LOCAL/.git ] && git clone $JEKYLL_GIT $JEKYLL_LOCAL

EXTRA_ARGS="-p $JEKYLL_PORT:80 -v $JEKYLL_LOCAL:$JEKYLL_SRC" ./run jekyll

echo "LOG: URL: http://$JEKYLL_HOST:$JEKYLL_PORT"
