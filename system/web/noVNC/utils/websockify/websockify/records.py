#!/usr/bin/env python

import os, re, time

class Records:
    def __init__(self, record_dir = 'recordings/', record_list = 'records.js', record_html = 'records.html', record_slice_size = 128):
	self.record_dir = record_dir
	self.record_list = record_list
	self.record_html = record_html
	# in KB
	self.record_slice_size = 128 * 1024

    def compare(self, x, y):
	stat_x = os.stat(self.record_dir + "/" + x)
	stat_y = os.stat(self.record_dir + "/" + y)
	if (stat_x.st_ctime > stat_y.st_ctime):
	    return -1
	elif (stat_x.st_ctime > stat_y.st_ctime):
	    return 1
	else:
	    return 0

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
	    print "Log: " + rec
	    if (rec == self.record_list or rec == self.record_html):
		continue;

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

	    info = {"create": '', "title": '', 'author': '', 'tags': '', 'desc': '', 'encoding': '', 'length': 0, 'time': 0, 'parts': 0, 'data_size': 0}
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
		if str(VNC_frame_time).isdigit():
		    VNC_frame_time = time.strftime("%H:%M:%S", time.gmtime(float(VNC_frame_time)/1000))
		    # print "LOG: < VNC_frame_time = %s" % VNC_frame_time

		# The size in string, not in binary
		# VNC_frame_data_size = len(repr(VNC_frame_data))

	    for (k, v) in info.items():
		val = eval("VNC_frame_%s" % k)
		if val:
		    info[k] = val

	    if not info['encoding']:
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

	    for k in ['data', 'data_compressed', 'data_part']:
		if globals().has_key('VNC_frame_%s' % k) or locals().has_key('VNC_frame_%s' % k):
		    exec("del VNC_frame_%s" % k)

	content += "];";

	records.write(content);
	records.close();
