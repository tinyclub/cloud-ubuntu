#!/usr/bin/env python

import os, re, time

class Records:
    def __init__(self, record_dir = 'recordings/', record_list = 'records.js', record_html = 'records.html'):
	self.record_dir = record_dir
	self.record_list = record_list
	self.record_html = record_html

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
	content += "  ['Name', 'Title', 'Size', 'Create', 'Author', 'Tags', 'Desc'],\n"

	rec_list = os.listdir(os.path.abspath(self.record_dir))
	# sort by time
	rec_list.sort(self.compare)

	num = 0;
	for rec in rec_list:
	    if (rec == self.record_list or rec == self.record_html):
		continue;

	    num += 1
	    f = os.path.abspath(self.record_dir + rec)
	    t = open(f)

	    frame_data_valid = 0
	    info = {"create": '', "title": '', 'author': '', 'tags': '', 'desc': ''}
	    for i in range(1, 20):
		l = t.readline()
		if not l:
		    break

		for (k, v) in info.items():
		    if not v:
			m = re.match(r"var VNC_frame_%s = '(.*)';" % k, l)
			if m and len(m.groups()):
			    info[k] = m.group(1)

	 	m = re.match(r"var VNC_frame_encoding = '(.*)';", l)
		if m and len(m.groups()):
		    frame_data_valid = 1

	    if not frame_data_valid:
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
		info['author'] = "anonymity"
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
		   "  ['%s', '%s', '%s%s', '%s', '%s', '%s', '%s'],\n" \
		   % (rec, info['title'], str(rec_size), unit,
		     info['create'], info['author'], info['tags'], info['desc'])

	content += "];";

	records.write(content);
	records.close();
