#!/usr/bin/env python
import praw
import random
import time
import json
import os
import re
import logging

from error.mode_error import ModeError


class Bot:
    def __init__(self, name: str = "imposterBot"):
        self.IGNORE = [
            "botwasnotanimposter",
            "drnhfm_bot",
            "Mattlam57",
            "MODdmhfm",
        ]
        logging.basicConfig(
            filename="bot.log",
            filemode="a",
            format="%(asctime)s:%(levelname)s => %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO,
        )
        self.reddit = praw.Reddit(name)
        self.start()

    def _get_user(self, message: str):
        regex = r"(?s).*\b(u\/[a-zA-Z0-9_-]+).*(\ssus(picious)?|\svent(ed|s)?|\simpost(er|or))(\s|\.|,|\?|!).*"
        match = re.match(regex, message, re.IGNORECASE)
        if match is not None:
            return match.group(1)
        return None

    def _manipC(self, mode="r", value=""):
        if mode == "r":
            with open("comm.json", "r", encoding="utf-8") as f:
                return json.load(f)
        elif mode == "w":
            with open("comm.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            data.append(value)
            with open("comm.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif mode == "i":
            if not os.path.exists("comm.json"):
                with open("comm.json", "w") as f:
                    json.dump([], f, indent=4, ensure_ascii=False)
        else:
            raise ModeError(f"Invalid mode: {mode}")

    def _search(self):
        for results in self.reddit.subreddit("all").comments():
            previous_id = self._manipC("r")
            body = results.body
            body = body.lower()
            comment_id = results.id
            if comment_id in previous_id or results.author.name in self.IGNORE:
                return
            user_name = self._get_user(body)
            if user_name is not None:
                logging.info(
                    f"Found comment with body:\n {body}\n by {results.author.name}"
                )
                print(f"Found comment with body:\n {body}\n by {results.author.name}")
                try:
                    if user_name.lower() in ["u/boidushya", "u/botwasnotanimposter"]:
                        results.reply(self._get_cust_resp(user_name))
                    else:
                        results.reply(self.get_resp(user_name))
                    self._manipC("w", comment_id)
                except Exception as e:
                    logging.error("Exception: ", exc_info=True)
                    print("Exception: ", exc_info=True)
                    break

    def _get_cust_resp(self, uN):
        botTag = "\n---\n\n^(Beep boop I'm a bot. Also I'm the imposter ok bye. Made by u/boidushya)"
        return (
            f"""
	. 　　　。　　　　•　 　ﾟ　　。 　　.

	　　　.　　　 　　.　　　　　。　　 。　. 　

	.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

	　　ﾟ　　 {uN} was ejected.　 。　.

	　　'　　　 Tough luck right?　 　　。

	　　ﾟ　　　.　　　. ,　　　　.　 .
	"""
            + botTag
        )

    def start(self):
        self._manipC("i")
        logging.info("Initialization complete! Looking for comments...")
        print("Initialization complete! Looking for comments...")
        while True:
            self._search()
            time.sleep(0.1)

    def get_resp(self, user_name: str):
        fChoice = random.randint(1, 2)
        sChoice = random.randint(0, 1)
        choice = [
            f"""
	. 　　　。　　　　•　 　ﾟ　　。 　　.

	　　　.　　　 　　.　　　　　。　　 。　. 　

	.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

	　　ﾟ　　 {user_name} was not {"An" if fChoice==2 else "The"} Impostor.　 。　.

	　　'　　　 {fChoice} Impostor{"s" if fChoice==2 else ""} remain{"s" if fChoice!=2 else ""} 　 　　。

	　　ﾟ　　　.　　　. ,　　　　.　 .
	""",
            f"""
	. 　　　。　　　　•　 　ﾟ　　。 　　.

	　　　.　　　 　　.　　　　　。　　 。　. 　

	.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•

	　　ﾟ　　 {user_name} was {"An" if sChoice==1 else "The"} Impostor.　 。　.

	　　'　　　 {sChoice} Impostor remains 　 　　。

	　　ﾟ　　　.　　　. ,　　　　.　 .
	""",
        ]
        botTag = "\n---\n\n^(Beep boop I'm a bot. Also I'm the imposter ok bye. Made by u/boidushya)"
        return random.choice(choice) + botTag


if __name__ == "__main__":
    bot = Bot()
