#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def is_special(filename):
  if len(re.findall(r'__\w+__', filename)) > 0:
    return True
  else:
    return False

def get_special_paths(dir_):
  special = []
  for file_cur in os.listdir(dir_):
    if is_special(file_cur):
      special.append(os.path.abspath(file_cur))
  for sp in special:
    print sp
  return special

def copy_to(paths, dest_dir):
  for path in paths:
    shutil.copy(path, dest_dir)

def zip_to(paths, zippath):
  cmd = 'zip -j ' + zippath + " " + " ".join(paths)
  print "Command I'm going to do:" + cmd

  status, output = commands.getstatusoutput(cmd)

  if status:
    sys.stderr.write(output)
    sys.exit(1)

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  special_files = get_special_paths(args[0])
  if todir:
    if os.path.isdir(todir) == False:
      os.mkdir(todir)
    copy_to(special_files, todir)
  if tozip:
    zip_to(special_files, tozip)

if __name__ == "__main__":
  main()
