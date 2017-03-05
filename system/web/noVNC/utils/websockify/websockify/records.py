#!/usr/bin/env python

import os, re, time, base64, zlib, binascii

class Records:
  def __init__(self, record_dir = 'recordings/', record_list = 'records.js',
      record_html = 'records.html', slice_size = 256, compress_level = 9,
      slice_str = '=-+-+=', min_frames = 35, max_frames = 45, time_zone='CST',
      action = ('remove', 'zb64', 'slice', 'restore_raw', 'remove_raw')):

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
    self.time_zone = time_zone

    self.raw = "raw"
    self.zb64 = "zb64"
    self.slice = "slice"
    self.slices = "slice."

  def suffix(self, rtype):
    return "." + rtype

  def abspath(self, path = '', rtype = ''):
    path = self.record_dir + path
    if rtype: path = path + self.suffix(rtype)
    #return os.path.abspath(path)
    return path

  def compare(self, x, y):
    stat_x = os.stat(self.abspath(x))
    stat_y = os.stat(self.abspath(y))
    if (stat_x.st_ctime > stat_y.st_ctime):
      return -1
    elif (stat_x.st_ctime > stat_y.st_ctime):
      return 1
    else:
      return 0

  def generate_zb64(self, rec, info, rtype = ''):
    data = info['data']
    if rtype == '': rtype = self.zb64

    orig = self.slice_str.join(data)
    info["data_size"] = len(orig)

    out = base64.b64encode(zlib.compress(orig, self.compress_level))
    info["data_compressed"] = out;

    in_size = len(repr(data))
    out_size = len(out)
    ratio = out_size*100 / in_size
    print "LOG:   Compress Ratio: %d%% (%d --> %d)" % (ratio, in_size, out_size)

    info['size'] = self.get_size_unit(out_size)

    zb_content = ""

    # .slice.x
    if rtype.find(self.slices) >= 0:
      zb_content += "var VNC_frame_size = '%s';\n" % info["size"]
      zb_content += "var VNC_frame_data_size = %s;\n" % info["data_size"]
    # .slice and .zb64
    else:
      for (k, v) in info.items():
        if k in ("slices", "data", "data_compressed"): continue
        if str(v).isdigit():
          zb_content += "var VNC_frame_%s = %s;\n" % (k, v)
        else:
          zb_content += "var VNC_frame_%s = '%s';\n" % (k, v)

    zb_content += "var VNC_frame_data_compressed = '%s';\n" % info["data_compressed"]

    f = self.abspath(rec, rtype)
    z = open(f, 'w+')
    z.write(zb_content)
    z.close()

    return out_size;

  def generate_slices(self, rec, info, slices):
    slice_index = 0
    slice_frame_start = 0
    slice_frame_end = 0
    slice_frame_length = info['length'] / slices;

    slice_content = ""
    for (k, v) in info.items():
      if k in ("data", "slices", "data_size", "data_compressed"): continue
      if str(v).isdigit():
        slice_content += "var VNC_frame_%s = %s;\n" % (k, v)
      else:
        slice_content += "var VNC_frame_%s = '%s';\n" % (k, v)

    data = info['data']

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
      #  slice_frame_end = info['length']

      print "LOG:   start: %d end: %d step: %d _end: %d" % (slice_frame_start, slice_frame_end, _slice_frame_length, info['length'])

      info['data'] = data[slice_frame_start:slice_frame_end]
      self.generate_zb64(rec, info, self.slices + "%d" % slice_index)

      slice_frame_start = slice_frame_end
      slice_index += 1

    print "LOG:   Total: %d, slices: %d" % (info['length'], slice_index)
    info['slices'] = slice_index
    slice_content += "var VNC_frame_%s = %d;\n" % ('slices', info['slices'])

    # Write slice index
    f = self.abspath(rec, self.slice)
    s = open(f, 'w+')
    s.write(slice_content)
    s.close()

  def get_size_unit(self, size):
    unit = ""
    if size > 1024:
      size = round(size / 1024.0, 1)
      unit = "K"
    if size > 1024:
      size = round(size / 1024.0, 1)
      unit = "M"
    if size > 1024:
      size = round(size / 1024.0, 1)
      unit = "G"
    return str(size) + unit

  def get_frame_time(self, frame):
    t = '00:00:00'
    m = re.match(r'[{}]([0-9]{1,})[{}]', frame)
    if m and len(m.groups()):
      t = time.strftime("%H:%M:%S", time.gmtime(float(m.group(1))/1000))

    return t

  def generate_raw(self, zb64):
    info = self.get_frame_info(zb64, self.zb64)
    if not info:
      print "LOG: Invalid zb64 data"
      return

    if info['create']:
      info['create'] = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.strptime(info['create'], "%Y%m%d %H:%M:%S")) + self.time_zone

    raw_content = ''
    for (k, v) in info.items():
      if k in ('data', 'size', 'slice_str', 'slices', 'data_size', 'data_compressed'): continue
      if str(v).isdigit():
        raw_content += "var VNC_frame_%s = %s;\n" % (k, v)
      else:
        raw_content += "var VNC_frame_%s = '%s';\n" % (k, v)

    raw_content += "var VNC_frame_%s = %r;\n" % ('data', info['data'])

    # Write raw session data
    f = self.abspath(zb64.replace(self.suffix(self.zb64), ''))
    s = open(f, 'w+')
    s.write(raw_content)
    s.close()

  def init_frame_info(self):
    info = {"create": '', "title": '', 'author': '', 'tags': '', 'desc': '', 'encoding': 'binary',
      'length': 0, 'time': 0, 'data': '',
      'size': '', 'slice_str': self.slice_str, 'slices': 0, 'data_size': 0, 'data': '', 'data_compressed': ''}
    return info

  def get_frame_info(self, rec, rtype):
    info = self.init_frame_info()

    for (k, v) in info.items():
      exec("VNC_frame_%s = ''" % k)

    f = self.abspath(rec)
    t = open(f)
    py_data = t.read().replace('var VNC_', 'VNC_')
    t.close()

    # Convert origin novnc session record data (javascript) to python code
    exec(py_data)

    key = 'VNC_frame_encoding'
    if globals().has_key(key) and locals().has_key(key):
      # already compressed data, ignore it.
      print "Invalid noVNC session data: %s" % rec
      return ''

    if rtype == 'raw':
      key = 'VNC_frame_data'
      if globals().has_key(key) or locals().has_key(key):
        VNC_frame_length = len(VNC_frame_data)
        VNC_frame_time = self.get_frame_time(VNC_frame_data[VNC_frame_length-2])
      else: return ''
    else:
      key = 'VNC_frame_data_compressed'
      if globals().has_key(key) or locals().has_key(key):
        VNC_frame_data = zlib.decompress(base64.b64decode(VNC_frame_data_compressed)).split(self.slice_str)
      else: return ''

    for (k, v) in info.items():
      val = eval("VNC_frame_%s" % k)
      if val: info[k] = val

    if not info['create']: info['create'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime(os.path.getctime(f)))
    elif rtype == 'raw': info['create'] = time.strftime("%Y%m%d %H:%M:%S", time.strptime(info['create'], "%a, %d %b %Y %H:%M:%S %Z"))

    if not info['title']: info["title"] = rec.replace(self.suffix(self.zb64), '')
    if not info['author']: info['author'] = "Unknown"
    if not info['tags']: info['tags'] = ""
    if not info['desc']: info['desc'] = ""

    # Get file size
    info['size'] = self.get_size_unit(os.path.getsize(f))

    return info

  def generate_list(self, info_list):
    content = "var VNC_record_player = '/play.html';\n"
    content += "var VNC_record_dir = '/%s';\n\n" % os.path.basename(self.record_dir.strip('/'))
    content += "var VNC_record_data = [ \n"
    content += "  ['Name', 'Title', 'Size', 'Time', 'Create', 'Author', 'Tags', 'Desc'],\n"
    content += info_list
    content += "];";

    # Save records list to self.record_list, by default, records.js
    r = open(self.abspath(self.record_list),'w+')
    r.write(content);
    r.close();

  def restore_raw(self):
    rec_list = os.listdir(self.abspath())
    rec_list.sort(self.compare)
    for rec in rec_list:
      if rec.find(self.suffix(self.zb64)) >= 0:
        raw_rec = rec.replace(self.suffix(self.zb64), '')
        if not os.path.exists(self.abspath(raw_rec)):
          print "LOG: Restore %s" % raw_rec
          self.generate_raw(rec)

  def remove_old(self):
    # list and sort by time
    rec_list = os.listdir(self.abspath())
    rec_list.sort(self.compare)
    for rec in rec_list:
      f = self.abspath(rec)
      if rec in (self.record_list, self.record_html) or rec.find(self.suffix(self.slice)) >= 0:
        print "LOG: Remove %s" % rec
        os.remove(f)
      if rec.find(self.suffix(self.zb64)) >= 0:
        raw_rec = rec.replace(self.suffix(self.zb64), '')
        if os.path.exists(self.abspath(raw_rec)):
          print "LOG: Remove %s" % rec
          os.remove(f)
        elif 'restore_raw' in self.action:
          print "LOG: Restore %s" % raw_rec
          self.generate_raw(rec)
          #print "LOG: Remove %s" % rec
          #os.remove(f)

  def generate(self):
    # Remove old record list, .zb64 and .slice*
    if 'remove' in self.action:
      self.remove_old()

    if 'restore_raw' in self.action:
      self.restore_raw()

    # Flash the list 
    rec_list = os.listdir(self.abspath())
    rec_list.sort(self.compare)

    # Grab the records info and generate files with zlib+base64 and if the
    # file is too big, slice it to several pieces.
    info_list = ""
    for rec in rec_list:
      # Ignore the .zb64 and .slice* and the record list file
      print "LOG: " + rec

      rtype = 'raw'
      if rec in (self.record_list, self.record_html): continue;
      if rec.find(self.suffix(self.slice)) >= 0: continue
      if rec.find(self.suffix(self.zb64)) >= 0 and rec.find(self.suffix(self.slice)) < 0:
        rtype = self.zb64
        if os.path.exists(self.abspath(rec.replace(self.suffix(rtype), ''))): continue

      # Grab frame info
      info = self.get_frame_info(rec, rtype)
      if not info: continue

      info_list += \
         "  ['%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'],\n" \
         % (rec, info['title'], info['size'], info['time'],
         info['create'], info['author'], info['tags'], info['desc'])

      # Generate xxx.zb64
      if rtype == self.raw:
        f = self.abspath(rec, self.zb64)
      if rtype == self.zb64:
        f = self.abspath(rec)

      out_size = 0
      if not os.path.exists(f):
        if 'zb64' in self.action:
          print "LOG:   Generate zb64"
          out_size = self.generate_zb64(rec, info)
      else:
        out_size = os.path.getsize(f)

      # Generate xxx.slice
      if rtype == self.zb64:
        rec = rec.replace(self.suffix(rtype), '')
      info['size'] = self.get_size_unit(out_size)
      if out_size and out_size > self.slice_size and 'slice' in self.action:
        if not os.path.exists(self.abspath(rec, self.slice)):
          print "LOG:   Generate slices"
          slices = out_size / self.slice_size + 1
          self.generate_slices(rec, info, slices)

      # Remove raw data, save the space
      if 'remove_raw' in self.action:
        f = self.abspath(rec)
        if os.path.exists(f):
          zb64 = self.abspath(rec + self.suffix(self.zb64))
          if not os.path.exists(zb64):
            print "LOG:   .zb64 doesn't exist, not remove raw data for security"
          else:
            print "LOG:   Remove raw data"
            os.remove(f)

    # Generate list
    if not info_list: return
    print "LOG: Generate %s" % self.record_list
    self.generate_list(info_list)
