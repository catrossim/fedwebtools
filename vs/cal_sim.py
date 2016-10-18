#!/usr/bin/env python
# coding: utf-8
import codecs
import os, sys
import logging
from operator import itemgetter
vmap = {}
def readvToDict(path):
    d = {}
    with codecs.open(path, 'r', 'utf-8') as f:
        line = f.readline()
        i = 1
        while line:
            line = line.split(' ')
            word, prob = line
            d[word] = dict(rank=i, prob=prob)
            if i>=1000:
                break
            i += 1
            line = f.readline()
    v = os.path.basename(path).split('.')[0]
    vmap[v] = d

def getVScore(words):
    result = {}
    for v in vmap.iterkeys():
        sum = 0
        vdict = vmap[v]
        for word in words:
            s = vdict.get(word, None)
            if s:
                sum += 1.0/s['rank']
        result[v] = sum
    return result

def begin(q_dir='expqs', v_dir='tfidfs', dest='rsim', eqc=10):
    # read information of verticals
    logging.info('q_dir: %s, v_dir: %s, dest: %s' %(q_dir, v_dir, dest))
    for fname in os.listdir(v_dir):
        readvToDict(os.path.join(v_dir, fname))
    logging.info('%s verticals were read.' %len(vmap))
    # read information of expanded queries
    q_files = [q for q in os.listdir(q_dir) if q.isdigit()]
    logging.info('%s files of expanded query were read.' %len(q_files))
    for q_file in q_files:
        exp_words = []
        with codecs.open(os.path.join(q_dir,q_file),'r','utf-8') as f:
            line = f.readline()
            wcount = 0
            while line:
                exp_words.append(line.split(' ')[0])
                wcount += 1
                if wcount == eqc:
                    break
                line = f.readline()
        r = getVScore(exp_words)
        sorted_r = sorted(r.items(),key=itemgetter(1),reverse=True)
        content = zip([a[0] for a in sorted_r],map(str, [a[1] for a in sorted_r]))
        with codecs.open(os.path.join(dest,q_file),'w','utf-8') as f:
            f.write('\n'.join([' '.join(x) for x in content]))
        logging.info('%s was finished.' %q_file)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    begin()
