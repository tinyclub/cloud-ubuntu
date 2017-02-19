#!/usr/bin/env python
#
# generate-records.py -- generate records.js for noVNC recordings in /noVNC/recordings/
#

import sys, os

mypath = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(mypath)

from records import *

def main():
    record_dir = ""
    if len(sys.argv) > 1:
        record_dir = sys.argv[1]
    if not record_dir:
        record_dir = mypath + "../../../../../../../" + "noVNC/recordings/"
    record_dir = os.path.abspath(record_dir) + "/"

    r = Records(record_dir)

    r.generate()

main()
