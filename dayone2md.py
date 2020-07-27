#!/usr/bin/env python
import json
import codecs
import sys
from datetime import datetime

tag_symbol = "#"

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print 'You need to pass a filename in argument like: ./dayone2md.py Journal.json'
    sys.exit()

filename = sys.argv[1]

fp = open(filename)
all = json.load(fp)

def entry2md(entry):
        date = datetime.strptime(entry['creationDate'],'%Y-%m-%dT%H:%M:%SZ')
        filename = date.strftime("%Y-%m-%d_%H-%m-%S")+".md"
        print filename

        text = "---\n"
        text += "title: " + "\n"
        text += "date: " + date.strftime("%Y-%m-%d")+"\n"
        
	tags = ""
	if 'tags' in entry.keys():
		for t in entry['tags']:
		    tag = " %s%s" %(tag_symbol,t)
                    if tag not in text:
                        tags += tag

	text += "tags: %s" %tags + "\n"

        if 'location' in entry.keys():
                text += "location: " + entry['location']['localityName'] +"\n"

        text += "---\n"

        if 'text' in entry.keys():
                text += "\n" + entry['text']

	text = text.replace("\.",".").replace("\(","(")\
                   .replace("\)",")").replace("\-","-")

        photos = dict()
	if 'photos' in entry.keys():
		for p in entry['photos']:
                        if 'md5' in p:
			    photos[p['identifier']] = "%s.%s" %(p['md5'],p['type'])
		for ph in photos:
			original = "![](dayone-moment://%s)" %ph
			new = "![](photos/%s)" %photos[ph]
			text = text.replace(original,new)

	fp = codecs.open("output/" + filename,'w','utf-8')
        fp.write(text)
        fp.close()

for entry in all['entries']:
    entry2md(entry)
