reddit_auto_poster
==================

A small bot to make regular posts on reddit

## Example config.ini

```
[DEFAULT]
users = {"Gharbad":"password"}
user_agent = /r/Diablo Weekly Thread Poster (/u/listen2)
tmp_prefix = /tmp

[loot]
subreddit = diablo
user = Gharbad
title = Official Loot Thread for the week of $date
week_num = 10
text = Welcome to week $count of the Official Weekly Loot Thread!

	Top three winners from last week's thread
	
	$winners
	
	[Last week's thread](/$last_thread).

[questions]
subreddit = diablo
user = Gharbad
title = Thursday Help Desk for $date. Ask your stupid questions here.
week_num = 6
text = Welcome to week $count of Thursday Help Desk.
	This is a weekly thread for any stupid/newbie/unsure questions you may have. No matter how dumb you may think the question is, now is your chance to have them answered.
```
