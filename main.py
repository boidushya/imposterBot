#!/usr/bin/env python
import praw
import random
import time
import json
import os
import re

class ModeError(Exception):
	pass

class Bot:
	def __init__(self,name="imposterBot"):
		self.reddit = praw.Reddit(name)
		self.start()

	def _getUser(self,message):
		regex = r"(?s).*(u\/\w+).*(sus|vent(ed|s)?|imposter).*"
		match = re.match(regex, message,re.IGNORECASE)
		if match != None:
			return match.group(1)
		return None

	def _manipC(self,mode="r",value=""):
		if mode=="r":
			with open("comm.json","r",encoding="utf-8") as f:
				return json.load(f)
		elif mode=="w":
			with open("comm.json", "r", encoding="utf-8") as f:
				data = json.load(f)
			data.append(value)
			with open("comm.json", "w", encoding="utf-8") as f:
				json.dump(data,f,indent=4,ensure_ascii=False)
		elif mode=="i":
			if not os.path.exists("comm.json"):
				with open("comm.json","w") as f:
					json.dump([],f,indent=4,ensure_ascii=False)
		else:
			raise ModeError(f"Invalid mode: {mode}")

	def _search(self):
		for results in self.reddit.subreddit("test").comments():
			previous_id = self._manipC("r")
			body = results.body
			body = body.lower()
			comment_id = results.id
			if comment_id in previous_id or results.author.name=="botwasnotanimposter":
				return
			userName = self._getUser(body)
			if userName != None:
				print(f"Found comment with body: {body} by {results.author.name}")
				try:
					results.reply(self.getResp(userName))
					self._manipC("w", comment_id)
				except Exception as e:
					print(str(e))
					break

	def start(self):
		self._manipC("i")
		print("Init complete! Looking for comments...")
		while True:
			self._search()
			time.sleep(2)

	def getResp(self,userName):
		fChoice = random.randint(1, 2)
		sChoice = random.randint(0, 1)
		choice = [f"""
	. 　　　。　　　　•　 　ﾟ　　。 　　.

	　　　.　　　 　　.　　　　　。　　 。　. 　

	.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

	　　ﾟ　　 {userName} was not {"An" if fChoice==2 else "The"} Impostor.　 。　.

	　　'　　　 {fChoice} Impostor{"s" if fChoice==2 else ""} remain{"s" if fChoice!=2 else ""} 　 　　。

	　　ﾟ　　　.　　　. ,　　　　.　 .
	""",
		f"""
	. 　　　。　　　　•　 　ﾟ　　。 　　.

	　　　.　　　 　　.　　　　　。　　 。　. 　

	.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

	　　ﾟ　　 {userName} was {"An" if sChoice==1 else "The"} Impostor.　 。　.

	　　'　　　 {sChoice} Impostor remains 　 　　。

	　　ﾟ　　　.　　　. ,　　　　.　 .
	"""]

		return random.choice(choice)

if __name__ == "__main__":
	bot = Bot()
