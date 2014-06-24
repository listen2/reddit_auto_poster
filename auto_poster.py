#!/usr/bin/python3

from string import Template
import configparser
import urllib.request
import datetime
import sys
import re
import lightreddit

cfg = configparser.ConfigParser()
cfg.read("config.ini")

r = lightreddit.RedditSession(cfg.get("DEFAULT", "user"), cfg.get("DEFAULT", "pass"), cfg.get("DEFAULT", "user_agent"))

thread_type = sys.argv[1]

try:
	with open("/tmp/diablo_thread_"+thread_type+"_tid", "r") as f:
		last_thread = f.read().rstrip()
except IOError:
	with open("/tmp/diablo_thread_"+thread_type+"_tid", "w") as f:
		last_thread = ""

title = Template(cfg.get(thread_type, "title"))
text = Template(cfg.get(thread_type, "text"))

class HeadRequest(urllib.request.Request):
	def get_method(self):
		return "HEAD"

def find_image(text):
	links = re.compile('&lt;a(.+)href="(.*)"(.+)&gt;', re.IGNORECASE)
	items = re.findall(links, text)

	img = urllib.request.urlopen(HeadRequest(items[0][1]))
	contentType = img.info()['Content-Type']

	if contentType != None and contentType.startswith('image/'):
		return items[0][1]

count = cfg.getint(thread_type, "week_num")

title = title.substitute(
	date=datetime.datetime.today().strftime("%m/%d/%y")
)
text = text.substitute(
	count=count,
	last_thread=last_thread
)

new_thread = r.submit(cfg.get("DEFAULT", "subreddit"), title, text, distinguish=True)
#print(text)

with open("/tmp/diablo_thread_"+thread_type+"_tid", "w") as f:
	f.write(new_thread.id)

cfg.set(thread_type, "week_num", str(count + 1))
with open("config.ini", "w") as config:
	cfg.write(config)
