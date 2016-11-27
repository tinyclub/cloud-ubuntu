#!/bin/bash
#
# jekyll.sh -- start the jekyll container
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

[ -z "$JEKYLL_GIT" ] && JEKYLL_GIT=https://github.com/plusjade/jekyll-bootstrap/
REPO_NAME=`basename $JEKYLL_GIT`

[ -z "$JEKYLL_LOCAL" ] && JEKYLL_LOCAL=${TOP_DIR}/$REPO_NAME/
[ -z "$JEKYLL_SRC" ] && JEKYLL_SRC=/home/ubuntu/$REPO_NAME/
[ -z "$JEKYLL_PORT" ] && JEKYLL_PORT=8080
[ -z "$JEKYLL_HOST" ] && JEKYLL_HOST=`ifconfig eth0 | grep "inet addr" | sed -e "s/ *inet addr:\([0-9\.]*\) .*/\1/g"`

[ ! -d $JEKYLL_LOCAL/.git ] && git clone $JEKYLL_GIT $JEKYLL_LOCAL

EXTRA_ARGS="-p $JEKYLL_PORT:8080 -v $JEKYLL_LOCAL:$JEKYLL_SRC -e JEKYLL_SRC=$JEKYLL_SRC" ./run jekyll

echo "LOG: URL: http://$JEKYLL_HOST:$JEKYLL_PORT"
