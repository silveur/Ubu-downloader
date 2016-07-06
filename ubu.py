from bs4 import BeautifulSoup
import urllib
import urllib2
import requests
import re
import os

r = urllib.urlopen('http://www.ubu.com/sound/').read()
soup = BeautifulSoup(r, 'html.parser')

artists = soup.find_all('a')

for artist in artists:
	link = 'http://www.ubu.com/sound/' + artist['href'].replace('./', '')
	ap = urllib.urlopen(link).read()
	soup = BeautifulSoup(ap, 'html.parser')
	links = soup.find_all('a', href=re.compile("\.mp3$"))
	for link in links:
		link = link['href'].encode('utf8')
		folder = artist.string.encode('utf8')
		index = link.rfind('/')
		trackName = link[index+1:]
		fullPath = './' + folder + '/' + trackName
		if not os.path.isfile(fullPath):
			print 'Downloading: ' + trackName
			rq = urllib2.Request(link)
			try:
				res = urllib2.urlopen(rq)
			except urllib2.HTTPError as e:
				print 'Request error: ' + link
			except urllib2.URLError as e:
				print 'URL error: ' + link
			else:
				if not os.path.exists(folder):
				    os.makedirs(folder)
				track = open( fullPath, 'wb')
				track.write(res.read())
				track.close()
				
		else:
			print 'Exist already: ' + trackName
