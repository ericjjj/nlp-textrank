#-*- encoding:utf-8 -*-
import jieba.posseg as pseg
import os
from collections import Counter,defaultdict
import codecs
import math
import numpy as np
import re

pos_tags      = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']
delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
stop_words    = []
filter_postag = lambda l: list(filter(lambda x: x.flag in pos_tags, l))
unique_list   = lambda x,y:x if y in x else x + [y]

class AttrDict(dict):
    """Dict that can get attribute by dot"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class TextRank(object):

  def __init__(self):
    self.text = ''
    self.tr = []
    self.stop_words = set()
    self.stop_words_file = get_default_stop_words_file()
    for word in codecs.open(self.stop_words_file, 'r', 'utf-8', 'ignore'):
        self.stop_words.add(word.strip())

  #
  def keywords(self, text, window=3, num=3):
    text = preprocess(text, self.stop_words)
    graph = keywordGraph(text, window)
    tr = textRank(graph)
    return tr[:num]

  def abstract(self, text):
    text = re.split('，|。|\n', text.encode("utf-8"))
    text = [w for w in text if len(w)>0]
    cut = []
    print '原文: \n', "\n".join(text)
    for item in text:
      cut.append(preprocess(item, self.stop_words))
    group = sum(cut, [])
    scores = []

    k1 = 2
    b = 0.75
    avg_dl = sum([len(item) for item in cut]) / len(cut)
    print avg_dl
    for d in cut:
      idf_arr = []
      r_arr = []
      dl = len(d)
      K = k1 * (1 - b + b * (dl / avg_dl))
      s = 0
      for qi in d:
        n = len([item for item in group if qi == item])
        idf = math.log(len(cut) - n + 0.5) - math.log(n + 0.5)
        idf_arr.append(idf)
        # print idf
        fi = len([item for item in d if item == qi])
        r = fi * (k1 + 1) / (fi + K)
        s += r
      print s, ', '.join(d)
      # s = sum(np.array(idf_arr) * np.array(r_arr))
      # scores.append(s)
    # for i in range(len(text)):
      # print scores[i], ': ', text[i]

    # def sim():
    #   pass

    # def simAll():
    #   pass

# 预处理
def preprocess(text, stop_words):
  # 分词
  text = pseg.cut(text)
  # 去除指定词性
  # text = filter_postag(text)
  # 去除标点符号
  text = [w.word.strip() for w in text if w.flag != 'x']
  # 去除空白
  text = [w for w in text if len(w)>0]
  # 去除停用词
  text = [word.strip() for word in text if word.strip() not in stop_words]
  # print ', '.join(text)
  return text

# 摘要图
def abstractGraph(word_list, window):
  data = defaultdict(Counter)
  # for i, words in enumerate(word_list):



# 关键词图
def keywordGraph(word_list, window):
  # 计数器, 统计每个单词出现频率
  data = defaultdict(Counter)
  for i,word in enumerate(word_list):
    # create window size
    indexStart = i - window
    indexEnd   = i + window
    # print 'begin', i, word, ", ".join(data[word])
    if indexStart < 0:
      temp = Counter(word_list[:window+1+i])
      temp.pop(word)
      data[word] += temp

    elif indexStart>=0 and indexEnd<=len(word_list):
      temp = Counter(word_list[i-window:i+window+1])
      temp.pop(word)
      data[word] += temp

    else:
      temp = Counter(word_list[i-window:])
      temp.pop(word)
      data[word]+=temp
    print "[", word, "]", ", ".join(data[word])
    # print data[word].items()
  return data

# 排名
def textRank(graph, d=0.85):
  # 初始权值为1
  TR = defaultdict(float,[(word, 1.) for word, cooc in graph.items()])
  # 收敛 100 次
  iter_no = 100

  for i in range(iter_no):
    for word, cooc in graph.items():
      temp = 0
      for link_word, weight in cooc.items():
        in_vi = TR[link_word]
        out_vj = sum(graph[link_word].values())
        temp += d * in_vi * weight / out_vj
      TR[word] = 1 - d + temp

  return [AttrDict(word= word, weight=weight) for word,weight in sorted(TR.iteritems(),key=lambda (k,v):(v,k),reverse=True)]

# 获取停用词文件
def get_default_stop_words_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')

