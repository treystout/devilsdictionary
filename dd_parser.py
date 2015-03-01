#!/usr/bin/env python
"""Parses the project gutenberg version of the devil's dictionary from plain
text into a python dictionary
"""
import re

RE_def = re.compile(r'^([A-Z]+?), (.{1,3})\.', re.M | re.S)

d = {}
words = []
with open("devilsdictionary.txt") as f:
  matches = RE_def.split(f.read())
  for i in range(1, len(matches), 3):
    if i > len(matches)-2:
      break
    word = matches[i].strip()
    part = matches[i+1].strip()
    definition = matches[i+2].strip()
    d[word] = {
        'part': part,
        'definition': definition
      }
    words.append({
        'word': word,
        'part': part,
        'definition': definition
      })

#for k, v in d.items():
#  print k, "->", v['definition']

#for w in words:
#  print "%s\t(%s.)" % (w['word'], w['part'])
#  print "\t|||%s|||\n" % w['definition']

for w in words:
  print "['%s', '%s', '''%s''']," % (w['word'], w['part'], w['definition'])
