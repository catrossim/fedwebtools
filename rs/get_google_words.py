#!/usr/bin/env python
# coding: utf-8
from rs_utils import readfilebylines, save
import os,sys

def getResponse(query):
    import requests
    r = requests.get(getUrl(query))
    return r.text

def getResponseAndSave(query, path):
    result = getResponse(query)
    save(path, result)
    print '[finish] %s' %os.path.basename(path)

def getUrl(query):
    url = ('https://www.googleapis.com/customsearch/v1?'
    'key=AIzaSyCDDz0RQURYSNNTyrmsoOxIXZbLVv1C6yg&'
    'q=%s&'
    'cx=001883590070454620361:c2r91kwg94s&'
    'fields=items(title,snippet)')%query.replace(' ','+')
    return url

if __name__ == '__main__':
    queries = sys.argv[1]
    dest = sys.argv[2]
    if len(sys.argv) < 3:
        print 'usage: ./get_google_words.py [queries] [dest]'
    from multiprocessing import Pool
    p = Pool()
    for line in readfilebylines(queries):
        qstring = line.strip().split('\t')
        p.apply_async(getResponseAndSave,args=(qstring[1],os.path.join(dest,qstring[0])))
    p.close()
    p.join()
