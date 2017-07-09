### 分析 TextRank4ZH 源码, 一共, 大概分三个步骤

1. 创建 Summary, Summary 中创建 Segmentation
  1. Segmentation 分别创建 词(Word)和段落(Sentence)
    1. 词: jieba
    2. 段落: 使用 '?,!' 等符号分段
    3. 为什么会分这两个部分? 下面 util 的函数中会用到, 对比相似度
2. 调用 analyze, 分段
  1. 调用 seg.segment (Segmentation),
    1. 调用 Sentence 中 segment, 分段, 返回 list
    2. 根据上面分段, 分状态(words_no_filter, words_no_stop_words, words_all_filters) 调用 Word 中的 segment_sentences, 然后 jieba
    3. 调用 util 的 AttrDict, 合并, (有点类似 Object.assign())
  2. 将上述结果根据所需, 赋值给 Segmentation, 调用  util.sort_sentences 排序,
    1. 创建 matrix
    2. 两层循环对比每句相似度 信息增益, get_similarity, 赋值 matrix
      1. list to matrix
      2. 计算概率 求对数
    3. 调用 networkx, matrix to graph
    4. 调用 nx.pagerank, 获取分数, 并进行排序
    5. 根据分数索引, 获取 sentence, return

3. 调用 get_key_sentences, 获取前 n 个摘要, 一般取第1个


### 其他
1. 关于 self.__dict__ = self https://stackoverflow.com/questions/39832721/meaning-of-self-dict-self-in-a-class-definition
