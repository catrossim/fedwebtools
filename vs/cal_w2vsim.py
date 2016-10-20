from WordGetter import WordGetter
import codecs, os, sys
from operator import itemgetter
import logging
def readvToDict(dir, vlimit):
    vmap = {}
    for fname in os.listdir(dir):
        d = {}
        with codecs.open(os.path.join(dir, fname), 'r', 'utf-8') as f:
            line = f.readline()
            i = 1
            while line:
                line = line.split(' ')
                word, prob = line
                d[word] = dict(rank=i, prob=prob)
                if i>=vlimit:
                    break
                i += 1
                line = f.readline()
        v = fname.split('.')[0]
        vmap[v] = d
    return vmap

def calW2vSim(wordgetter, words, vmap):
    result = {}
    wordslen = len(words)
    for v in vmap.iterkeys():
        sum = 0
        vdict = vmap[v]
        for word in words:
            for key in vdict.iterkeys():
                try:
                    score = wordgetter.similarity(word,key)
                except KeyError, arg:
                    logging.warn(arg)
                    score = 0
                sum += score
        result[v] = sum/wordslen
    return result

def getExpWords(path, limit=10):
    exp_words = []
    with codecs.open(path,'r','utf-8') as f:
        line = f.readline()
        wcount = 0
        while line:
            exp_words.append(line.split(' ')[0])
            wcount += 1
            if wcount>limit:
                break
            line = f.readline()
    return exp_words

def save(path,content):
    with codecs.open(path,'w','utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    model_path = 'enwiki_nltk/wiki.en.text.model'
    q_dir = 'expqs'
    v_dir = 'tfidfs'
    wordgetter = WordGetter(model_path)
    vlimit = int(sys.argv[1]) if len(sys.argv)>1 else 200
    dest = 'rsim_w2v_'+str(vlimit)
    logging.info('q_dir: %s, v_dir: %s, dest: %s' %(q_dir, v_dir, dest))
    if not os.path.exists(dest):
        os.mkdir(dest)
        logging.info('%s created' %dest)
    vmap = readvToDict(v_dir, vlimit)
    logging.info('%s verticals were read.' %len(vmap))
    q_files = [file for file in os.listdir(q_dir) if file.isdigit()]
    logging.info('%s queries were loaded.' %len(q_files))
    for q_file in q_files:
        exp_words = getExpWords(os.path.join(q_dir,q_file))
        result = calW2vSim(wordgetter, exp_words, vmap)
        sorted_r = sorted(result.items(),key=itemgetter(1),reverse=True)
        content = zip([a[0] for a in sorted_r],map(str, [a[1] for a in sorted_r]))
        save(os.path.join(dest, q_file), '\n'.join([' '.join(x) for x in content]))
