from gensim.models import LdaModel
from codecs import open as open
from multiprocessing import Pool
import os, sys
def load_model(path):
    return LdaModel.load(path)

def save(path, content):
    with open(path, 'w', 'utf-8') as f:
        f.write(content)

def get_topn_words_and_save(path, dest):
    model_name = os.path.basename(path)+'.model'
    lda_model = load_model(os.path.join(path,model_name))
    wordmap = lda_model.id2word
    topics = [token[0] for token in lda_model.show_topics(-1)]
    destpath = os.path.join(dest,os.path.basename(path))
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    for t in topics:
        r = [(wordmap[x[0]],str(x[1])) for x in lda_model.get_topic_terms(t,30)]
        save(os.path.join(destpath, str(t)), '\n'.join([' '.join(x) for x in r]))

if __name__ == '__main__':
    src = sys.argv[1]
    dest = sys.argv[2]
    if not os.path.exists(dest):
        os.mkdir(dest)
    p = Pool()
    for d in os.listdir(src):
        if d.startswith('e'):
            p.apply_async(get_topn_words_and_save, args=(os.path.join(src,d), dest))
    p.close()
    p.join()
