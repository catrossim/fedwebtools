#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os.path,sys
from bs4 import BeautifulSoup, SoupStrainer

reload(sys)
sys.setdefaultencoding('utf-8')

vtoe = {}

def readetovMapping(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            token = line.split(' ')
            v = token[1].strip()
            e = token[0].strip()
            if vtoe.get(v) is None:
                vtoe[v] = []
                vtoe[v].append(e)
            else:
                vtoe[v].append(e)

def normpath(path):
    if path.find('~') != -1:
        # replace the '~' with $HOME
        path = os.path.expanduser(path)
    else:
        path = os.path.normpath(os.path.abspath(path))
    return path

def handleSrc(path, destDir):
    for v in vtoe.iterkeys():
        for e in vtoe.get(v):
            eSrc = os.path.join(path, e, e+'.xml')
            # print eSrc
            if os.path.exists(eSrc):
                logging.info('Ready to parse %s' % eSrc)
                result = _handleFile(eSrc)
                logging.info('Finish parsing %s, number of tokens is %d' % (eSrc,len(result)))
                saveResult(os.path.join(destDir, v), e, ' '.join(result))

def _handleFile(path):
    soup = BeautifulSoup(open(path), 'xml', parse_only=SoupStrainer('snippet'))
    # print soup.prettify().encode('utf-8')
    results = []
    for snippet in soup.select('snippet'):
        # print snippet.select('title')
        title = snippet.title.string.strip()
        description = snippet.description.string.strip()
        # print '%s\n%s'%(title, description)
        tokens = _tokenizeAll(title, description)
        results.extend(tokens)
    return results

def _tokenizeAll(*posts):
    result = []
    for post in posts:
        if post is not None:
            result.extend(tokenize(post))
    return result

def tokenize(post):
    from nltk import word_tokenize, stem
    from nltk.corpus import stopwords
    import string
    if isinstance(post, unicode):
        post = str(post)
    # 转化为小写
    text = post.lower()
    # 移除标点
    no_punctuation = text.translate(None, string.punctuation)
    # 分词
    tokens = word_tokenize(no_punctuation)
    # 词干提取
    stemmer = stem.SnowballStemmer('english')
    stem_tokens = [stemmer.stem(x) for x in tokens if x not in stopwords.words('english')]
    return stem_tokens

def saveResult(destDir, fileName, content):
    if not os.path.exists(destDir):
        os.mkdir(destDir)
    with open(os.path.join(destDir, fileName),'w') as f:
        f.write(content)

def multiHandleDir(dirList):
    pass

class FileNotFoundError(Exception):
    pass

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logging.info("running %s" % ' '.join(sys.argv))
    if len(sys.argv) != 3:
        print 'usage ./vs.py [src] [dest]'
        sys.exit()
    srcDir = sys.argv[1]
    destDir = sys.argv[2]
    # 读入垂直领域与资源库关系
    readetovMapping(normpath('ev-mapping.txt'))
    # processNum = 4
    # dirs = [[] for i in xrange(processNum)]
    # i = 0
    # keys = [x for x in vtoe.iterkeys()]
    # while i<processNum:
    #     dirs[i] = [x for x in keys if keys.index(x)%processNum==i]
    #     i = i + 1
    # for vList in dirs:
    #     multiHandleDir(vList)
    #     pass
    # srcDir: 所有资源库所属的上一级文件夹

    if not os.path.exists(srcDir):
        print 'src is not exists: %s' %srcDir
        sys.exit()
    if not os.path.exists(destDir):
        try:
            os.mkdir(destDir)
        except Exception:
            logging.error('Error in mkdir: %s' % destDir)
    # 处理资源库文件
    handleSrc(normpath(srcDir),destDir)
