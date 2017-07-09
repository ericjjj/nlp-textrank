#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from libs import Summary

text = codecs.open('./test/01.txt', 'r', 'utf-8').read()

s = Summary()
s.analyze(text=text, lower=True, source = 'all_filters')

print()
print( '摘要：' )
for item in s.get_key_sentences(num=3):
    print(item.index, item.weight, item.sentence)
