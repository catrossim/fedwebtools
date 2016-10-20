#!/usr/bin/env python
from WordGetter import WordGetter
import sys,os,logging
from StopWordHandler import StopWordHandler
from nltk import stem
stopwords = None
wordgetter=None

def init(path):
    global wordgetter
    wordgetter = WordGetter(path)
    global stopwords
    stopwords = StopWordHandler('stop_words.utf8')

def preprocess_query(query):
    extra_filter = ['21st','mp3']
    stemmer = stem.SnowballStemmer('english')
    query = query.replace('-',' ').strip()
    words = [stemmer.stem(x.lower()) for x in query.split(' ') \
        if not stopwords.exist(x.lower()) and not x.isdigit() and x.lower() not in extra_filter]
    return words

def get_similar_words(words):
    return wordgetter.most_similar(words)

def save(path,content):
    import codecs
    with codecs.open(path,'w','utf-8') as f:
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
            num = line.split('\t')[0]
            words = preprocess_query(query)
            probs = [1 for i in xrange(len(words))]
            simwords = zip(words, probs)
            try:
                simwords.append(get_similar_words(words))
            except KeyError, arg:
                logging.error('KeyError: %s %s' %(arg, num))
                continue
            r = zip([a[0] for a in simwords],map(str,[a[1] for a in simwords]))
            result = '\n'.join([' '.join(x) for x in r])
            save(os.path.join(dest_dir,num), result)
