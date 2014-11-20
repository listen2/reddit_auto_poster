#!/usr/bin/python3

from string import Template
import configparser
import datetime
import sys
import lightreddit

cfg = configparser.ConfigParser()
config_file = sys.argv[1]
cfg.read(config_file)

r = lightreddit.RedditSession(cfg.get("DEFAULT", "user"), cfg.get("DEFAULT", "pass"), cfg.get("DEFAULT", "user_agent"))

thread_type = sys.argv[2]

try:
	with open("/tmp/diablo_thread_"+thread_type+"_tid", "r") as f:
		last_thread = f.read().rstrip()
except IOError:
	with open("/tmp/diablo_thread_"+thread_type+"_tid", "w") as f:
		last_thread = ""

title = Template(cfg.get(thread_type, "title"))
text = Template(cfg.get(thread_type, "text"))

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
