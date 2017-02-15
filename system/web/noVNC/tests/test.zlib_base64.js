/*

#!/usr/bin/env python

import sys, os, base64, zlib, binascii

mypath = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(mypath)

from vnc_session_data import *

def main():
	orig = ','.join(VNC_frame_data)
	print "orig.length = %s" % len(orig)

	# compress it with zip+base64
	out = base64.b64encode(zlib.compress(orig, 9))
	#out = '%r' % zlib.compress(orig, 9)
	print "comp.length = %s" % len(out)

main()
*/

// play.html can use this directly.

function decompress_base64encoded_zlib_compressed_data() {
	var compstr = Base64.decode("eJxLSxsyILW8hCqgHAgAS65mkw==");
	var zlib = new Inflator.Inflate();
	var uint8arr = zlib.inflate(compstr);
	var decompstr = String.fromCharCode.apply(null, uint8arr);

	console.info(decompstr);
}
