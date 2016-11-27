#!/bin/bash
#
# jekyll.sh -- start the jekyll container
#

TOP_DIR=$(cd $(dirname $0) && pwd)/../

JEKYLL_GIT=https://github.com/plusjade/jekyll-bootstrap/
JEKYLL_LOCAL=${TOP_DIR}/jekyll-bootstrap/
JEKYLL_SRC=/home/ubuntu/jekyll-bootstrap/

[ ! -d $JEKYLL_LOCAL/.git ] && git clone $JEKYLL_GIT $JEKYLL_LOCAL

EXTRA_ARGS="-v $JEKYLL_LOCAL:$JEKYLL_SRC" ./run jekyll
