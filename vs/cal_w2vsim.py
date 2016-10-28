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

def calW2vSim(wordgetter, words, vmap, handler):
    result = {}
    wordslen = len(words)
    for v in vmap.iterkeys():
        sum = 0
        vdict = vmap[v]
        for word in words:
            for key in vdict.iterkeys():
                try:
                    score = wordgetter.similarity(word,key)
                except KeyError:
                    score = 0
                sum = handler(sum,score)
        result[v] = sum/wordslen
    return result

def sum(a,b):
    return a+b

def findmax(a,b):
    return max(a,b)

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

def normalize(scores):
    result = []
    max = scores[0][1]
    min = scores[len(scores)-1][1]
    for s in scores:
        result.append((s[0],(s[1]-min)*1.0/(max-min)))
    return result

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    if len(sys.argv)<6:
        print 'usage: python cal_w2vsim.py <model> <query> <verticals> <wl> <vl>'
        sys.exit(1)
    model_path = sys.argv[1]
    q_dir = sys.argv[2]
    v_dir = sys.argv[3]
    wlimit = int(sys.argv[4])
    vlimit = int(sys.argv[5])
    wordgetter = WordGetter(model_path)
    dest = '{}_{}_{}'.format('w2vsim',wlimit,vlimit)
    logging.info('q_dir:{}, v_dir:{}, dest:{}, wlimit:{}, vlimit:{}'.format(
            q_dir,
            v_dir,
            dest,
            wlimit,
            vlimit
        ))

    if not os.path.exists(dest):
        os.mkdir(dest)
        logging.info('%s created' %dest)

    vmap = readvToDict(v_dir, vlimit)
    logging.info('%s verticals were read.' %len(vmap))

    q_files = [file for file in os.listdir(q_dir) if file.isdigit()]
    logging.info('%s queries were loaded.' %len(q_files))

    for q_file in q_files:
        exp_words = getExpWords(os.path.join(q_dir,q_file),wlimit)
        result = calW2vSim(wordgetter, exp_words, vmap, findmax)
        sorted_r = sorted(result.items(),key=itemgetter(1),reverse=True)
        # sorted_r = normalize(sorted_r)
        content = zip([a[0] for a in sorted_r],map(str, [a[1] for a in sorted_r]))
        save(os.path.join(dest, q_file), '\n'.join([' '.join(x) for x in content]))
        logging.info('%s finished.' %q_file)
