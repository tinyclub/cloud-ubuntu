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

    # 0: zb64 + slice
    # 1: zb64
    # 2: remove + zb64
    # 3: remove + zb64 + slice

    action = 0
    if len(sys.argv) > 2:
        action = int(sys.argv[2])

    if not record_dir:
        record_dir = mypath + "../../../../../../../" + "noVNC/recordings/"
    record_dir = os.path.abspath(record_dir) + "/"

    if action == 1:
	action = ('zb64',)
    elif action == 2:
	action = ('remove', 'zb64')
    elif action == 3:
	action = ('remove', 'zb64', 'slice')
    elif action == 4:
	action = ('remove', 'zb64', 'slice', 'remove_raw')
    else:
	action = ('zb64', 'slice')

    r = Records(record_dir, action = action)

    r.generate()

main()
