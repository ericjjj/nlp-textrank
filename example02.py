#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from libs import Abstract

text = codecs.open('./test/03.txt', 'r', 'utf-8').read()
w = Abstract()
rank = w.abstract(text)
print(rank)
print(', '.join(rank))

# for item in rank:
   # print(item.word, item.weight)
