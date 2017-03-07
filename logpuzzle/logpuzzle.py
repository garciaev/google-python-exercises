#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

"""Returns a list of the puzzle urls from the given log file,
extracting the hostname from the filename itself.
Screens out duplicate urls and returns the urls sorted into
increasing order."""

def byword_key(urlname):
    return urlname.split('-')[-1]

def read_urls(filename):
    servername = 'http://' + filename.split('_')[1]
    pagename = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if 'puzzle' in line and 'jpg' in line:
                pagename.append(servername
                          + line[line.find('GET'):line.find('HTTP')].
                          strip('GET '))

    pagename = sorted(set(pagename), key=byword_key)
    return pagename


def download_images(img_urls, dest_dir):
    """
     Given the urls already in the correct order, downloads
     each image into the given directory.
     Gives the images local filenames img0, img1, and so on.
     Creates an index.html in the directory
     with an img tag to show each local image file.
     Creates the directory if necessary.
    """
    if os.path.isdir(dest_dir) == False:
        os.mkdir(dest_dir)

    url_img_string = ""
    for j, img_url in enumerate(img_urls):
        print 'Retrieving ' + img_url + ' ...'

        img_loc = dest_dir + '/img' + str(j)
        urllib.urlretrieve(img_url, img_loc)
        url_img_string = url_img_string + '<img src="' \
                         + os.path.abspath(img_loc) + '">'
    # Now make the index.html file
    with open(dest_dir + '/index.html', 'w') as f:
        f.write('<verbatim>' + '\n')
        f.write('<html>' + '\n')
        f.write('<body>' + '\n')
        f.write(url_img_string + '\n')
        f.write('</body>' + '\n')
        f.write('</html>' + '\n')
    f.close()


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
