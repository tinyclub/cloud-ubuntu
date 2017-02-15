#!/usr/bin/env python

import os, re, time, base64, zlib, binascii

class Records:
    def __init__(self, record_dir = 'recordings/', record_list = 'records.js', \
		record_html = 'records.html', slice_size = 512, compress_level = 9, \
		slice_str = '^_^', min_frames = 35):
	self.record_dir = record_dir
	self.record_list = record_list
	self.record_html = record_html
	# in KB
	self.slice_size = slice_size * 1024
	self.compress_level = compress_level
	self.slice_str = slice_str
	# Ensure frames eough for play several seconds
	self.min_frames = min_frames

    def compare(self, x, y):
	stat_x = os.stat(self.record_dir + "/" + x)
	stat_y = os.stat(self.record_dir + "/" + y)
	if (stat_x.st_ctime > stat_y.st_ctime):
	    return -1
	elif (stat_x.st_ctime > stat_y.st_ctime):
	    return 1
	else:
	    return 0

    def generate_zb64(self, rec, data, info, suffix = ".zb64"):
	out = ''
	orig = ''
	del info["data_size"]
	del info["data_compressed"]

	slice_str = self.slice_str;
	orig = slice_str.join(data)
	info["data_size"] = len(orig)

	out = base64.b64encode(zlib.compress(orig, self.compress_level))
	info["data_compressed"] = out;

	in_size = len(repr(data))
	out_size = len(out)
	ratio = out_size*100 / in_size
	print "  LOG: Compress Ratio: %d%% (%d --> %d)" % (ratio, in_size, out_size)
	out = ''
	orig = ''

	zb_content = ""
	if suffix.find('.slice.') < 0:
	    for (k, v) in info.items():
		if str(v).isdigit():
		    zb_content += "var VNC_frame_%s = %s;\n" % (k, v)
		else:
		    zb_content += "var VNC_frame_%s = '%s';\n" % (k, v)
	else:
	    zb_content += "var VNC_frame_data_size = %s;\n" % info["data_size"]
	    zb_content += "var VNC_frame_data_compressed = '%s';\n" % info["data_compressed"]

	f = os.path.abspath(self.record_dir + rec + suffix)
	t = open(f, 'w+')
	t.write(zb_content)
	t.close()

	return out_size;


    def generate(self):
	records = open(os.path.abspath(self.record_dir + self.record_list),'w+')

	content = "var VNC_record_player = '/play.html';\n"
	content += "var VNC_record_dir = '/%s';\n\n" % os.path.basename(self.record_dir.strip('/'))
	content += "var VNC_record_data = [ \n"
	content += "  ['Name', 'Title', 'Size', 'Time', 'Create', 'Author', 'Tags', 'Desc'],\n"

	rec_list = os.listdir(os.path.abspath(self.record_dir))
	# sort by time
	rec_list.sort(self.compare)

	num = 0;
	for rec in rec_list:
	    print "LOG: " + rec
	    if (rec == self.record_list or rec == self.record_html):
		continue;
	    if (rec.find(".zb64") >= 0 or rec.find(".slice") >= 0):
		continue

	    num += 1
	    f = os.path.abspath(self.record_dir + rec)
	    t = open(f)

	    # Init the variables: VNC_frame_xxx
	    # VNC_frame_data_size/VNC_frame_data_compressed
	    #
	    # data size have different meanings:
	    #   0. the whole file size, include the header variables
	    #   1. original data size in string
	    #   2. array data size in binary
	    #   3. joined array data size for compress (required by client for decompression)
	    #   4. data size after compression
	    for k in ['data', 'data_compressed']:
		if globals().has_key('VNC_frame_%s' % k) or locals().has_key('VNC_frame_%s' % k):
		    exec("del VNC_frame_%s" % k)

	    info = {"create": '', "title": '', 'author': '', 'tags': '', 'desc': '', 'encoding': '', \
		'length': 0, 'time': 0, 'slice_str': self.slice_str, 'slices': 0, 'data_size': 0, 'data_compressed': ''}
	    for (k, v) in info.items():
		exec("VNC_frame_%s = ''" % k)

	    # Convert to python code
	    py_data = t.read().replace('var VNC_', 'VNC_')
	    exec(py_data)

	    if globals().has_key('VNC_frame_data') or locals().has_key('VNC_frame_data'):
		# The number of frames
	        VNC_frame_length = len(VNC_frame_data)
		# print "LOG: VNC_frame_length = %s" % VNC_frame_length

		# Match strings like '{62911{\x00@' or '}304}RFB 003.008' to get out of the timestamp
		m = re.match(r'[{}]([0-9]{1,})[{}]',VNC_frame_data[VNC_frame_length-2])
		if m and len(m.groups()):
		    VNC_frame_time = time.strftime("%H:%M:%S", time.gmtime(float(m.group(1))/1000))
		    # print "LOG: > VNC_frame_time = %s" % VNC_frame_time
	    else:
		#if str(VNC_frame_time).isdigit():
		#    VNC_frame_time = time.strftime("%H:%M:%S", time.gmtime(float(VNC_frame_time)/1000))
		    # print "LOG: < VNC_frame_time = %s" % VNC_frame_time
		t.close()
		continue;

		# The size in string, not in binary
		# VNC_frame_data_size = len(repr(VNC_frame_data))

	    for (k, v) in info.items():
		val = eval("VNC_frame_%s" % k)
		if val:
		    info[k] = val

	    if info['data_size']:
		# already compressed data, ignore it.
		print "Invalid noVNC session data: %s" % rec
		t.close()
		continue

	    if not info['encoding']:
		# encoding is necessary for the raw data.
		print "Invalid noVNC session data: %s" % rec
		t.close()
		continue

	    if not info['create']:
		info['create'] = time.strftime("%Y%m%d %H:%M:%S",
			     time.localtime(os.path.getctime(f)))
	    else:
		info['create'] = time.strftime("%Y%m%d %H:%M:%S",
			     time.strptime(info['create'], "%a, %d %b %Y %H:%M:%S %Z"))
	    if not info['title']:
		info["title"] = rec
	    if not info['author']:
		info['author'] = "Unknown"
	    if not info['tags']:
		info['tags'] = ""
	    if not info['desc']:
		info['desc'] = ""

	    t.close()

	    rec_size = os.path.getsize(f)
	    raw_size = rec_size
	    unit = ""
	    if rec_size > 1024:
		rec_size = round(rec_size / 1024.0, 1)
		unit = "K"

	    if rec_size > 1024:
		rec_size = round(rec_size / 1024.0, 1)
		unit = "M"

	    content += \
		   "  ['%s', '%s', '%s%s', '%s', '%s', '%s', '%s', '%s'],\n" \
		   % (rec, info['title'], str(rec_size), unit, info['time'],
		     info['create'], info['author'], info['tags'], info['desc'])

	    # Generate xxx.zb64
	    out_size = self.generate_zb64(rec, VNC_frame_data, info)

	    # Generate xxx.slice
	    if out_size > self.slice_size:
		slices = out_size / self.slice_size + 1

		# Write first slice
		slice_index = 0
		slice_frame_start = 0
		slice_frame_end = 0
		slice_frame_length = VNC_frame_length / slices;

		while (slice_frame_end < VNC_frame_length):
		    _slice_frame_length = slice_frame_length
		    if (slice_index == 0 and slice_frame_length < self.min_frames):
			_slice_frame_length = self.min_frames

		    slice_frame_end = slice_frame_start + _slice_frame_length - 1
		    if (slice_frame_end > VNC_frame_length):
			slice_frame_end = VNC_frame_length
		    elif ((VNC_frame_length - slice_frame_end) < self.min_frames):
			slice_frame_end = VNC_frame_length

		    print "  LOG: start: %d end: %d step: %d _end: %d" % (slice_frame_start, slice_frame_end, _slice_frame_length, VNC_frame_length)

		    out_size = self.generate_zb64(rec, VNC_frame_data[slice_frame_start:slice_frame_end], info, ".slice.%d" % slice_index)
		    print "  LOG: %s: From %s to %s" % (rec, slice_frame_start, slice_frame_end)

		    #slice_content = ""
		    #f = os.path.abspath(self.record_dir + rec + ".slice.%d" % slice_index)
		    #t = open(f, 'w+')
		    #slice_conetent = "var VNC_fame_data_slize = "
		    #t.write(slice_content)
		    #t.close()

		    slice_frame_start = slice_frame_end
		    slice_index += 1

		slices = slice_index
		print "  LOG: Total: %d, slices: %d" % (VNC_frame_length, slices)
		info['slices'] = slices

		slice_content = ""
	        for (k, v) in info.items():
		    if (k == "data_size" or k == "data_compressed"):
			continue

		    if str(v).isdigit():
			slice_content += "var VNC_frame_%s = %s;\n" % (k, v)
		    else:
			slice_content += "var VNC_frame_%s = '%s';\n" % (k, v)

		# Write slice index
		f = os.path.abspath(self.record_dir + rec + ".slice")
		t = open(f, 'w+')
		t.write(slice_content)
		t.close()

	content += "];";

	records.write(content);
	records.close();
