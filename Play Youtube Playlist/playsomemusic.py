#!/usr/bin/env python
# Author: pabloheralm@gmail.com
#         @pablololo12

import sys
import getopt
import re
import os
import requests
import errno
import urlparse
import socket
import subprocess
import shlex
import time
import json
from select import select
from socket import error as socket_error
import tty
try:
	from subprocess import DEVNULL  # Python 3.
except ImportError:
	DEVNULL = open(os.devnull, 'wb')

# Transform message into JSON
def compose_message(message):
	data = json.dumps(message, separators=",:")
	return data.encode("utf8", "strict") + b"\n"

# Gets info from a video
def get_name(video):
	html = requests.get(video).text
	for name in re.findall('''title":["'](.[^"']+)["']''', html, re.I):
		return name

	return "Unknown"

def play_music(list):
	
	tty.setcbreak(sys.stdin.fileno())
	i = 0
	while 1:
		proc = subprocess.Popen(shlex.split("mpv " + list[i] + " --no-video\
					--quiet --input-ipc-server=.mpvsocket"), stdout=DEVNULL)
		soc = 0
		while 1:
			try:
				soc = socket.socket(socket.AF_UNIX)
				soc.connect(".mpvsocket")
				break
			except socket_error:
				continue

		print(get_name(list[i]))
		while 1:
			ch=0
			rlist, _, _ = select([sys.stdin], [], [], 0.1)
			if rlist:
				ch = sys.stdin.read(1)
			elif proc.poll() is not None:
				break
			else:
				continue
			if ch == 'q':
				soc.send(compose_message({"command": ["quit"]}))
				proc.kill()
				soc.shutdown(socket.SHUT_WR)
				soc.close()
				os.remove(".mpvsocket")
				sys.exit()
				break
			elif ch in 'l':
				soc.send(compose_message({"command": ["seek", "5"]}))
			elif ch in 'j':
				soc.send(compose_message({"command": ["seek", "5"]}))
			elif ch in 'n':
				soc.send(compose_message({"command": ["quit"]}))
				proc.kill()
				soc.shutdown(socket.SHUT_WR)
				soc.close()
				break
			elif ch in 'b':
				soc.send(compose_message({"command": ["quit"]}))
				proc.kill()
				soc.shutdown(socket.SHUT_WR)
				soc.close()
				i = i-2
				break
			elif ch in '\ ':
				soc.send(compose_message({"command": ["cycle", "pause"]}))

		os.remove(".mpvsocket")
		i = i + 1
		if i < 0:
			i = len(list) - 1
		elif i >= len(list):
			i = 0

def get_webpage(url):
	return requests.get(url).text

def get_videos(html):
	id_list = []
	for numID in re.findall('''href="/watch\?v=(.[^&]+)&''', html, re.I):
		id_list.append("https://www.youtube.com/watch?v="+numID)

	return list(set(id_list))

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hu:")
	except getopt.GetoptError:
		print("playsomemusic.py [-h | -u [url]]")
		sys.exit(2)

	url = 0
	for opt, arg in opts:
		if opt == '-h':
			print("-h to help")
			print("-u [url] to insert the url directly")
			sys.exit()
		elif opt == '-u':
			url = arg

	if url == 0:
		url = raw_input("Please enter playlist url: ")

	print("\nControls:")
	print("  space: play/pause")
	print("  j/l: backward/forward")
	print("  n: next song")
	print("  b: previous song")
	print("  q: to exit\n\n")

	html = get_webpage(url)
	id_list = get_videos(html)

	if len(id_list) == 0:
		sys.exit(2l)
	play_music(id_list)


if __name__ == '__main__':
    main(sys.argv[1:])