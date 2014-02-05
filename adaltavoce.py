import os
import feedparser
import urllib
import hashlib

# podcast downloader for "Ad Alta Voce" radio transmission

BASE_FOLDER_NAME = "AD_ALTA_VOCE/"
AD_ALTA_VOCE_FEED = "http://www.radio.rai.it/radio3/podcast/rssradio3.jsp?id=272"

def clean_s(s):
  for i in xrange(len(s)-1,0,-1):
	if s[i] == "/":
	  return s[i+1:]

def download_files(d):
  for i in d.entries:
	print "* Downloading",i.title,"from",i.link,"..."
	directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), BASE_FOLDER_NAME)
	filename = os.path.join(directory, clean_s(i.link))
	if os.path.exists(filename):
	  print "*** *** *** File already downloaded."
	else:
	  print "** Saving in",filename
	  urllib.urlretrieve(i.link,filename)
	

path = os.path.dirname(BASE_FOLDER_NAME)
print path
if not os.path.exists(path):
  os.mkdir(path)

print "Fetching data..."
raw_d = feedparser.parse(AD_ALTA_VOCE_FEED)
print "Done."
s = ""
for i in raw_d.entries:
  s += i.title + i.link
hush = hashlib.md5()
hush.update(s)
h = hush.hexdigest()
print "Checking hashes..."
try:
  check = file(BASE_FOLDER_NAME+"hush","r")
  print "Hash file found. Checking..."
  data = check.readlines()
  if data[0] == h:
	print "md5: OK"
  else:
	print "md5: DIFFERENT"
	download_files(raw_d)
	checknew = file(BASE_FOLDER_NAME+"hush","w")
	checknew.write(h)
	print "md5 wrote on file."
except(IOError):
  download_files(raw_d)
  check = file(BASE_FOLDER_NAME+"hush","w")
  check.write(h)
  print "md5 wrote on file."