#!/usr/bin/env python

import os, re, time

class Records:
    def __init__(self, record_dir = 'recordings/', record_list = 'records.html'):
        self.record_dir = record_dir
        self.record_list = record_list

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
        content = "<html>\n" \
                  "<head>\n" \
                  "<title>noVNC Recordings</title>\n" \
                  "<style style='text/css'>\n" \
                  "    a { text-decoration: none; outline: none; }\n" \
                  "    table { border: 1px solid #333; border-spacing: 0; border-collapse: collapse; width: 100%; }\n" \
                  "    th, td { padding-left: 2px; padding-right: 2px; padding-top: 10px; padding-bottom: 10px;\n" \
                  "             border: 1px solid #aaa; display: table-cell; \n" \
                  "             text-align: center; max-width: 100px; }\n" \
                  "    td { font-size: 80%; overflow: hidden; text-overflow: ellipsis } \n" \
                  "    tr.head { background-color: #ccc; } \n" \
                  "    tr.odd { background-color: #eee; } \n" \
                  "    tr.even { background-color: #fff; } \n" \
                  "    tr:hover { background-color: #aaa; } \n" \
                  "</style>\n" \
                  "</head>\n" \
                  "<body>\n\n"
 
        content += "<table>\n" \
                   "  <tr class='head'>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "    <th>%s</th>\n" \
                   "  </tr>\n" \
                   % ("No.", "Play", "Down", "Title", "Size",
                     "Time", "Author", "Tags", "Desc")
   
        rec_list = os.listdir(os.path.abspath(self.record_dir))
        # sort by time
        rec_list.sort(self.compare)

        num = 0;
        for rec in rec_list:
            if (rec == self.record_list):
                continue

            num += 1
            f = os.path.abspath(self.record_dir + rec)
            t = open(f)

            info = {"time": '', "title": '', 'author': '', 'tags': '', 'desc': ''}
            for i in range(1, 10):
                l = t.readline()
                if not l:
                    break

                for (k, v) in info.items():
                    if not v:
                        m = re.match(r"var VNC_frame_%s = '(.*)';" % k, l)
                        if m and len(m.groups()):
                            info[k] = m.group(1)

            if not info['time']:
                info['time'] = time.strftime("%Y%m%d %H:%M:%S",
                             time.localtime(os.path.getctime(f)))
            else:
                info['time'] = time.strftime("%Y%m%d %H:%M:%S",
                             time.strptime(info['time'], "%a, %d %b %Y %H:%M:%S %Z"))
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
        
            play_url = "/play.html?data=" + rec
            down_url = "/" + self.record_dir + rec

            bg = "even"
            if num % 2:
                bg = "odd"

            content += \
                   "  <tr class='%s'>\n" \
                   "    <td>%s</td>\n" \
                   "    <td><a href='%s' target='_top' title='play'> &gt; </a></td>\n" \
                   "    <td><a href='%s' target='_blank' title='download'> v </a></td>\n" \
                   "    <td><span title='%s'>%s</span></td>\n" \
                   "    <td><span title='%s%s'>%s%s</span></td>\n" \
                   "    <td><span title='%s'>%s</span></td>\n" \
                   "    <td><span title='%s'>%s</span></td>\n" \
                   "    <td><span title='%s'>%s</span></td>\n" \
                   "    <td><span title='%s'>%s</span></td>\n" \
                   "  </tr>\n" \
                   % (bg, num, play_url, down_url, info['title'], info['title'],
                     str(rec_size), unit, str(rec_size), unit,
                     info['time'], info['time'], info['author'], info['author'],
                     info['tags'], info['tags'], info['desc'], info['desc'])

        content += "</table>\n\n" \
                   "</body>\n" \
                   "</html>"

        records.write(content);
        records.close();
