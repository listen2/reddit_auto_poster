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

if len(sys.argv) != 2:
	print("Usage: %s thread_type" % (sys.argv[0]))
	sys.exit(1)

thread_type = sys.argv[1]
passwd = eval(cfg.get("DEFAULT", "users"))
tmp_prefix = cfg.get("DEFAULT", "tmp_prefix")
rname = cfg.get(thread_type, "subreddit")
uname = cfg.get(thread_type, "user")

tmp_file = "%s/%s_thread_%s_tid" % (tmp_prefix, rname, thread_type)

r = lightreddit.RedditSession(uname, passwd[uname], cfg.get("DEFAULT", "user_agent"))

with open(tmp_file, "r") as f:
	last_thread = f.read().rstrip()

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

winners = ""
if (thread_type == "loot"):
	comments = r.get_thread(last_thread).comments
	comments.append(lightreddit.RedditComment(r, {"kind":"t3", "data":{"author":None, "body":""}}))	#ensure we always have at least three
	comments.append(lightreddit.RedditComment(r, {"kind":"t3", "data":{"author":None, "body":""}}))
	comments.append(lightreddit.RedditComment(r, {"kind":"t3", "data":{"author":None, "body":""}}))
	winners_data = r.get_thread(last_thread).comments[3:]

	winners = Template("""1st: [$win1_name]($win1_userpage) :: [Item]($win1_link)

2nd: [$win2_name]($win2_userpage) :: [Item]($win2_link)

3rd: [$win3_name]($win3_userpage) :: [Item]($win3_link)
	""")

	winners = winners.substitute(
		win1_name = winners_data[0].author.name,
		win1_userpage = winners_data[0].author.name,
		win1_link = find_image(winners_data[0].body),
		win2_name = winners_data[1].author.name,
		win2_userpage = winners_data[1].author.name,
		win2_link = find_image(winners_data[1].body),
		win3_name = winners_data[2].author.name,
		win3_userpage = winners_data[2].author.name,
		win3_link = find_image(winners_data[2].body),
	)
	winners = "[Winners from last week could not be displayed]"

title = title.substitute(
	date=datetime.datetime.today().strftime("%m/%d/%y")
)
text = text.substitute(
	count=count,
	last_thread=last_thread,
	winners=winners
)

new_thread = r.submit(rname, title, text, distinguish=True)
#print(text)

with open(tmp_file, "w") as f:
	f.write(new_thread.id)

cfg.set(thread_type, "week_num", str(count + 1))
with open("config.ini", "w") as config:
	cfg.write(config)
