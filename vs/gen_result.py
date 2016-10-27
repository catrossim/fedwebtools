#!/usr/bin/env python
# coding: utf-8
import codecs,os,sys
import logging
GENERAL_SRC = 'v001'
QUESTION_WORDS = ['who','why','what','when','how','where']
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
    if len(sys.argv)<4:
        print 'usage: python genresult.py <src> <runtag> <esp>'
        sys.exit(1)
    source = sys.argv[1]
    dest = sys.argv[2]
    esp = float(sys.argv[3])
    output = []
    readQTerms()
    for fname in os.listdir(source):
        count = 0
        with codecs.open(os.path.join(source,fname),'r','utf-8') as f:
            flag = False
            if findQWords(fname):
                logging.info('%s has question-word. Send it to GENERAL' %fname)
                output.append(FORMAT_STR.format(fname,'FW14-'+GENERAL_SRC,dest))
                count += 1
                flag = True
            for line in f.readlines():
                tokens = line.split(' ')
                if tokens[1] == '0':
                    break
                if float(tokens[1].strip()) > esp:
                    if flag and tokens[0]==GENERAL_SRC:
                        continue
                    output.append(FORMAT_STR.format(fname,'FW14-'+tokens[0],dest))
                    count += 1
            if not count:
                logging.info('%s has no suitable topics. Send it to GENERAL' %fname)
                output.append(FORMAT_STR.format(fname,GENERAL_SRC,dest))
                count += 1
    with codecs.open(dest, 'w', 'utf-8') as f:
        f.write('\n'.join(output))
