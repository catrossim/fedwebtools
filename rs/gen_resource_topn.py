#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import LdaModel
from multiprocessing import Pool
from rs_utils import save
import os, sys, logging
logger = logging.getLogger('gen_resource_topn')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_model(path):
    return LdaModel.load(path)

def get_topn_words_and_save(path, dest, topn):
    logger.info('%s begin' %path)
    model_name = os.path.basename(path)+'.model'
    lda_model = load_model(os.path.join(path,model_name))
    wordmap = lda_model.id2word
    topics = [token[0] for token in lda_model.show_topics(-1)]
    destpath = os.path.join(dest,os.path.basename(path))
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    for t in topics:
        r = [(wordmap[x[0]],str(x[1])) for x in lda_model.get_topic_terms(t,topn)]
        save(os.path.join(destpath, str(t)), '\n'.join([' '.join(x) for x in r]))
    logger.info('%s finish' %path)

if __name__ == '__main__':
    if len(sys.argv)<3:
        print 'usage: ./gen_resource_topn.py <src> <dest> <n>'
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    n = sys.argv[3]
    if not os.path.exists(dest):
        os.mkdir(dest)
    p = Pool()
    for d in os.listdir(src):
        if d.startswith('e'):
            p.apply_async(get_topn_words_and_save, args=(os.path.join(src,d), dest, int(n)))
    p.close()
    p.join()
