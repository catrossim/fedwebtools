#!/usr/bin/env python
# coding: utf-8
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
import codecs

def tokenize(post):
    from nltk import word_tokenize
    return word_tokenize(post)

def get_sorted_index(arr,eps=1e-4):
    new_arr = []
    sorted = []
    for a in xrange(len(arr)):
        if arr[a]>eps:
            new_arr.append(arr[a])
            sorted.append(a)

    for i in xrange(len(new_arr)-1):
        j = len(new_arr)-1
        while j>i:
            if new_arr[j]>new_arr[i]:
                swap(new_arr,i,j)
                swap(sorted,i,j)
            j = j-1
    return sorted

def swap(arr,i,j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

corpus = []
target = 'vtext'
s = []
logging.info('Ready to read sources from %s' % target)
for path,dir,files in os.walk(target):
    for file in files:
        if file.endswith('.text'):
            with open(os.path.join(path,file),'rU') as f:
                corpus.append(f.read())
            s.append(file)
if not corpus:
    logging.error('Can not find corpus')
    import sys
    sys.exit(1)

logging.info('Source reading complete!')

def save_file(path, content):
    logging.info('saving content to %s' % path)
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(content)
    logging.info('file %s save' % path)

dest = 'result'

v = TfidfVectorizer(tokenizer=tokenize)
logging.info('Begin to calculate tf-idf...')
result = v.fit_transform(corpus).toarray()
logging.info('Successfully get tf-idf vector!')
words = v.get_feature_names()

for r in xrange(len(result)):
    output = []
    logging.info('Begin to sort %s...' % r)
    sorted_index = get_sorted_index(result[r])
    logging.info('Sorted %s' %r)
    for i in sorted_index:
        output.append(words[i]+' '+str(result[r][i]))
    save_file(os.path.join(dest,s[r]+'.words'), '\n'.join(output))
