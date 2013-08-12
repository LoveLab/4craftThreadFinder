#! /usr/bin/env python3
# Created 2013-08-06
# 20130806-07 20130809-11
# todo: auto-saving threads, opening links in a browser, revise boards

import sys
import re
import time
from urllib.request import urlopen

sleep_time = 900
boards = ["v", "b", "r9k", "k", "a", "x", "vg", "mlp", "tg", "c", "vr", "m", \
	"int", "soc", "jp", "u", "h", "g", "po", "o", "mu", "an", "fit", "d", \
	"s4s", "gif", "e", "sci", "s", "asp"]
thread_links = []
regex_pattern_keyword="4craft"

def Download(url):
	""" Returns downloaded data """
	try:
		temp = urlopen(url)
	except:
		# try again
		try:
			temp = urlopen(url)
		except:
			return False
	else:
		data = temp.read()
		temp.close()
		data = str(data)
		return data

def Parse(board, threads_ids_only, threads_contents):
	""" Looks for threads/posts with regex_pattern_keyword in them. \
		Adds links to relevant threads to thread_links. """
	if re.search(regex_pattern_keyword, threads_contents) != None:
		bool_in_ops_msg = False
		board_link = "http://boards.4chan.org/" + board

		for thread_id in threads_ids_only:
			thread_link = "http://boards.4chan.org/" + board + "/res/" +\
				thread_id
			regex_pattern="\{\"no\":" + thread_id + ".*?\"replies\":"
			thread_ops_msg = re.findall(regex_pattern, threads_contents)

			if re.search(regex_pattern_keyword, thread_ops_msg[0]) != None and \
				thread_links.count(thread_link) == 0:
				thread_links.append(thread_link)
				print(thread_link)
				bool_in_ops_msg = True

		if bool_in_ops_msg == False and thread_links.count(board_link) == 0:
			thread_links.append(board_link)
			print(board_link)

def main():
	print("Searching for \"", regex_pattern_keyword, "\" on ", sep='', end='')

	for board in boards:
		print("/", board, "/ ", sep='', end='')

	print("\n")

	while True:
		for board in boards:
			threads_ids = Download("http://api.4chan.org/" + board + \
				"/threads.json")
			time.sleep(1)
			threads_contents = Download("http://api.4chan.org/" + board + \
				"/catalog.json")
			threads_ids = None
			if threads_ids == False or threads_ids == None or \
				threads_contents == False or threads_contents == None:
				break
				print("yeah")
				sys.exit()
			print("hue")

			threads_ids_only = re.findall("(?<=\"no\"\:)[0-9]*(?=\,\")", \
				threads_ids)
			Parse(board, threads_ids_only, threads_contents)
			time.sleep(2)
		time.sleep(sleep_time)
main()
