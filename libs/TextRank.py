#-*- encoding:utf-8 -*-
import jieba.posseg as pseg
import os
from collections import Counter,defaultdict
import codecs

pos_tags      = ['ns', 'n', 'vn', 'v']
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

  def analyze(self, text, window=3, num=20):
    # 分词
    text = pseg.cut(text)
    # 去除指定词性
    text = filter_postag(text)
    # 去除标点符号
    text = [w.word.strip() for w in text if w.flag != 'x']
    # 去除空白
    text = [w for w in text if len(w)>0]
    # 去除停用词
    text = [word.strip() for word in text if word.strip() not in self.stop_words]
    graph = createGraph(text, window)
    tr = textRank(graph)
    self.text = text
    self.tr = tr
    return tr[:num]

# 图
def createGraph(word_list, window):
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
    # print word, ", ".join(data[word])
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

def get_default_stop_words_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')

