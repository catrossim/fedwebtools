#!/usr/bin/env python
from WordGetter import WordGetter
import sys,os
from StopWordHandler import StopWordHandler
stopwords = None
wordgetter=None

def init(path):
    global wordgetter
    wordgetter = WordGetter(path)
    global stopwords
    stopwords = StopWordHandler('stop_words.utf8')

def preprocess_query(query):
    words = [x.lower() for x in query.split(' ') if not stopwords.exist(x.lower())]
    return words

def get_similar_words(words):
    return wordgetter.most_similar(words)

def save(path,content):
    with open(path,'w') as f:
        f.write(content)

if __name__ == '__main__':
    if len(sys.argv)<4:
        print 'usage: ./query_expand.py [model_file] [query_file] [dest_dir]'
        sys.exit(1)
    path = sys.argv[1]
    query_path = sys.argv[2]
    dest_dir = sys.argv[3]
    init(path)
    with open(query_path, 'r') as f:
        for line in f.readlines():
            query = line.split('\t')[1]
            words = preprocess_query(query)
            result = '\n'.join([' '.join(x) for x in get_similar_words(words)])
            save(os.path.join(dest_dir,query[0]), result)
