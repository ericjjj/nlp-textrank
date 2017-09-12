#-*- encoding:utf-8 -*-
import jieba.posseg as pseg
import os
from collections import Counter,defaultdict
import codecs
import math
import numpy as np
import re
import operator
from .TextRank import TextRank


class Abstract(object):

  def __init__(self):
    self.text = ''

  #
  def abstract(self, text, window=3, num=3):
    graph = sentence_coocurance(text)
    result = abstractTextRank(graph)
    return result


def sentence_coocurance(text,kw_num=3):
  docs = re.split(u'，|。',text)
  sentence_kw = defaultdict(list)
  for sen in docs:
    if sen == '':
      continue
    w = TextRank()
    rank = w.keywords(sen)
    keywords = [item.word for item in rank]
    sentence_kw[sen] = keywords

  cooc_dict = defaultdict(dict) # coocurance sentence with respect to keywords

  for sentence,kw in sentence_kw.items():
    print sentence, ', '.join(kw)
    temp = {}
    for sent_check, kw_check in sentence_kw.items():
      if sentence == sent_check:

        temp[sentence] =0
        continue
      else:
        count = 0
        for word in kw:
          if word in kw_check:
            count+=1
        # print 'yes:\t',coun
        temp[sent_check] = count
    cooc_dict[sentence] = temp
  return cooc_dict

def abstractTextRank(graph, d=0.85, sent_num=3):
  sent_TR = defaultdict(float,[(sent,np.random.rand()) for sent,_ in graph.items()])

  err = 1e-5
  error = 1
  iter_no = 100
  index = 1
  while (iter_no >index and  error > err):
    error = 0
    sent_TR_prev = sent_TR.copy()
    for sent,cooc in graph.items():
        temp = 0
        for link_sent,weight in cooc.items():
          t = sum(graph[link_sent].values())
          t = 1 if t == 0 else t
          temp += d*sent_TR[link_sent]*weight/t

        sent_TR[sent] = 1 -d + temp
    error += (sent_TR[sent] - sent_TR_prev[sent])**2

    # print 'key sentence finding...iter_no:{},\terror:{}'.format(index,error)
    index += 1
    ks = [sent for sent,weight in sorted(sent_TR.iteritems(),key=lambda (k,v):(v,k),reverse=True)[:sent_num]]
  return ks
