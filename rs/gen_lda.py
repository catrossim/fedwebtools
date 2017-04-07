from codecs import open as open
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from multiprocessing import Pool
from rs_utils import readfilebylines
import logging, sys, os

logger = logging.getLogger('gen_lda')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logging.root.setLevel(logging.INFO)

def tokenize(doc):
    return doc.strip().split(' ')

def trainmodel(path):
    corpus = readfilebylines(path)
    logger.info('%s files were loaded.' %len(corpus))
    processed_docs = [tokenize(c) for c in corpus]
    word_count_dict = Dictionary(processed_docs)
    logger.info('%s words in origin.' %len(word_count_dict))
    word_count_dict.filter_extremes(no_below=3, no_above=0.1)
    logger.info('%s words remained after filetering.' %len(word_count_dict))
    bag_of_words_corpus = [word_count_dict.doc2bow(pdoc) for pdoc in processed_docs]
    lda_model = LdaModel(
        corpus=bag_of_words_corpus,
        id2word=word_count_dict,
        passes=5,
        num_topics=50)
    return lda_model, word_count_dict

def trainmodel_and_save(src, dest, fname):
    model, wmap = trainmodel(os.path.join(src,fname))
    dname = os.path.join(dest,fname)
    if not os.path.exists(dname):
        os.mkdir(dname)
    model.save(os.path.join(dname,fname+'.model'))
    wmap.save(os.path.join(dname,fname+'.wordmap'))
    logger.info('%s finished.' %fname)

if __name__ == '__main__':
    if len(sys.argv)<3:
        print 'usage: ./gen_lda.py <src> <dest>'
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    if not os.path.exists(dest):
        os.mkdir(dest)
    p = Pool()
    for fname in os.listdir(src):
        if fname.startswith('e'):
            p.apply_async(trainmodel_and_save, args=(src, dest, fname,))
            # trainmodel_and_save(src, dest, fname)
    p.close()
    p.join()
