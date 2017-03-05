#!/usr/bin/env python

import os, re, time, base64, zlib, binascii

class Records:
    def __init__(self, record_dir = 'recordings/', record_list = 'records.js', \
		record_html = 'records.html', slice_size = 256, compress_level = 9, \
		slice_str = '=-+-+=', min_frames = 35, max_frames = 45, action = ('remove', 'zb64', 'slice', 'remove_raw')):
	self.record_dir = record_dir
	self.record_list = record_list
	self.record_html = record_html
	# in KB
	self.slice_size = slice_size * 1024
	self.compress_level = compress_level
	self.slice_str = slice_str
	# Ensure frames eough for play several seconds
	self.min_frames = min_frames
	self.max_frames = max_frames
	self.action = action

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
	z = open(f, 'w+')
	z.write(zb_content)
	z.close()

	return out_size;

    def generate_slices(self, rec, data, info, slices):
	# Write first slice
	slice_index = 0
	slice_frame_start = 0
	slice_frame_end = 0
	slice_frame_length = info['length'] / slices;

	while (slice_frame_end < info['length']):
	    _slice_frame_length = slice_frame_length
	    if slice_index == 0:
		if slice_frame_length < self.min_frames:
		    _slice_frame_length = self.min_frames
		if slice_frame_length > self.max_frames:
		    _slice_frame_length = self.max_frames

	    slice_frame_end = slice_frame_start + _slice_frame_length - 1
	    if (slice_frame_end > info['length']):
		slice_frame_end = info['length']
	    #elif ((info['length'] - slice_frame_end) < self.min_frames):
	    #    slice_frame_end = info['length']

	    print "  LOG: start: %d end: %d step: %d _end: %d" % (slice_frame_start, slice_frame_end, _slice_frame_length, info['length'])

	    out_size = self.generate_zb64(rec, data[slice_frame_start:slice_frame_end], info, ".slice.%d" % slice_index)
	    print "  LOG: %s: From %s to %s" % (rec, slice_frame_start, slice_frame_end)

	    slice_frame_start = slice_frame_end
	    slice_index += 1

	print "  LOG: Total: %d, slices: %d" % (info['length'], slice_index)
	info['slices'] = slice_index

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
	s = open(f, 'w+')
	s.write(slice_content)
	s.close()

    def get_file_size(self, fname):
        rec_size = os.path.getsize(fname)
	raw_size = rec_size
	unit = ""
	if rec_size > 1024:
	    rec_size = round(rec_size / 1024.0, 1)
	    unit = "K"
	if rec_size > 1024:
	    rec_size = round(rec_size / 1024.0, 1)
	    unit = "M"
	return str(rec_size) + unit

    def generate_raw(self, zb64):
	info = {"create": '', "title": '', 'author': '', 'tags': '', 'desc': '', 'encoding': 'binary', \
		'length': 0, 'time': 0, 'data': ''}
	for (k, v) in info.items():
	    exec("VNC_frame_%s = ''" % k)

	f = zb64.replace(".zb64","")
	t = open(zb64)
	py_data = t.read().replace('var VNC_', 'VNC_')
	t.close()

	exec(py_data)
	if not VNC_frame_data_compressed:
	    return

	info['data'] = zlib.decompress(base64.b64decode(VNC_frame_data_compressed)).split(self.slice_str)

	if not info['title']:
	    info["title"] = os.path.basename(f)

	if not info['length']:
	    info['length'] = len(info['data'])

	    if not info['time']:
		m = re.match(r'[{}]([0-9]{1,})[{}]', info['data'][info['length']-2])
		if m and len(m.groups()):
		    info['time'] = time.strftime("%H:%M:%S", time.gmtime(float(m.group(1))/1000))

	if not info['create']:
	    info['create'] = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(time.time()))

	raw_content = ''
	for (k, v) in info.items():
	    if str(v).isdigit():
		raw_content += "var VNC_frame_%s = %s;\n" % (k, v)
	    elif k == 'data':
		raw_content += "var VNC_frame_%s = %r;\n" % (k, v)
	    else:
		raw_content += "var VNC_frame_%s = '%s';\n" % (k, v)

	# Write raw session data
	s = open(f, 'w+')
	s.write(raw_content)
	s.close()

    def generate(self):
	content = "var VNC_record_player = '/play.html';\n"
	content += "var VNC_record_dir = '/%s';\n\n" % os.path.basename(self.record_dir.strip('/'))
	content += "var VNC_record_data = [ \n"
	content += "  ['Name', 'Title', 'Size', 'Time', 'Create', 'Author', 'Tags', 'Desc'],\n"

	# list and sort by time
	rec_list = os.listdir(os.path.abspath(self.record_dir))
	rec_list.sort(self.compare)

	if 'remove' in self.action:
	    for rec in rec_list:
		absrec = os.path.abspath(self.record_dir + rec)
		if rec in (self.record_list, self.record_html):
		    print "LOG: Remove %s" % rec
		    os.remove(absrec)
		if rec.find(".zb64") >= 0 or rec.find(".slice") >= 0:
		    if os.path.exists(self.record_dir + rec.replace(".zb64", "").replace(".slice", "")):
		        print "LOG: Remove %s" % rec
			os.remove(absrec)
		    elif rec.find(".zb64") >= 0:
		        print "LOG: Restore raw %s" % rec.replace(".zb64", "")
			self.generate_raw(absrec)
		        #print "LOG: Remove %s" % rec
			#os.remove(absrec)
	    # flash the list and ignore the .zb64 and .slice* and the record list file
	    rec_list = os.listdir(os.path.abspath(self.record_dir))
	    rec_list.sort(self.compare)

	# grab the records info and generate files with zlib+base64 and if the
	# file is too big, slice it to several pieces.
	for rec in rec_list:
	    print "LOG: " + rec
	    if rec in (self.record_list, self.record_html):
		continue;
	    if (rec.find(".zb64") >= 0 or rec.find(".slice") >= 0):
		continue

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

	    # Convert origin novnc session record data (javascript) to python code
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

	    # Close the file
	    t.close()

	    # Get file size
	    size = self.get_file_size(f)

	    # Remove raw data, save the space
	    if 'remove_raw' in self.action:
		print "LOG: Remove %s" % f
		os.remove(f)

	    content += \
		   "  ['%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'],\n" \
		   % (rec, info['title'], size, info['time'],
		     info['create'], info['author'], info['tags'], info['desc'])

	    # Generate xxx.zb64
	    if 'zb64' in self.action:
		f = os.path.abspath(self.record_dir + rec + ".zb64")
		if not os.path.exists(f):
		    out_size = self.generate_zb64(rec, VNC_frame_data, info)
		else:
		    out_size = os.path.getsize(f)

	    # Generate xxx.slice
	    if out_size > self.slice_size and 'slice' in self.action:
		if not os.path.exists(self.record_dir + rec + ".slice"):
		    slices = out_size / self.slice_size + 1
		    self.generate_slices(rec, VNC_frame_data, info, slices)

	content += "];";

	# Save records list to self.record_list, by default, records.js
	r = open(os.path.abspath(self.record_dir + self.record_list),'w+')
	r.write(content);
	r.close();
