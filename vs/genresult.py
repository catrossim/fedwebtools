#!/usr/bin/env python
# coding: utf-8
import codecs,os
import logging
GENERAL_SRC = 'FW14-v001'
QUESTION_WORDS = ['what','when','how','where']
FORMAT_STR = '{} {} {}'
qterms = {}

def readQTerms():
    with codecs.open('queryterms.txt','r','utf-8') as f:
        for line in f.readlines():
            tokens = line.split('\t')
            qterms[tokens[0]] = tokens[1]
def findQWords(name):
    for w in QUESTION_WORDS:
        if qterms.get(name).find(w)>=0:
            return True
    return False

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    dest = 'kapokrun1'
    source = 'rsim'
    esp=1e-2
    output = []
    readQTerms()
    for fname in os.listdir(source):
        count = 0
        with codecs.open(os.path.join(source,fname),'r','utf-8') as f:
            if findQWords(fname):
                logging.info('%s has question-word. Send it to GENERAL' %fname)
                output.append(FORMAT_STR.format(fname,GENERAL_SRC,dest))
                count += 1
            for line in f.readlines():
                tokens = line.split(' ')
                if tokens[1] == '0':
                    break
                if float(tokens[1].strip()) > esp:
                    output.append(FORMAT_STR.format(fname,'FW14-'+tokens[0],dest))
                    count += 1
            if not count:
                logging.info('%s has no suitable topics. Send it to GENERAL' %fname)
                output.append(FORMAT_STR.format(fname,GENERAL_SRC,dest))
                count += 1
    with codecs.open(dest, 'w', 'utf-8') as f:
        f.write('\n'.join(output))
