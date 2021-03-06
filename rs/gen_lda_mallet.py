from codecs import open as open
from gensim.corpora import Dictionary
from gensim.models.wrappers import LdaMallet as LdaModel
from multiprocessing import Pool
from rs_utils import readfilebylines
import logging, sys, os

logger = logging.getLogger('gen_lda_mallet')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logging.root.setLevel(logging.INFO)

def tokenize(doc):
    return doc.strip().split(' ')

def trainmodel(mpath, cpath):
    corpus = readfilebylines(cpath)
    logger.info('%s files were loaded.' %len(corpus))
    processed_docs = [tokenize(c) for c in corpus]
    word_count_dict = Dictionary(processed_docs)
    logger.info('%s words in origin.' %len(word_count_dict))
    # word_count_dict.filter_extremes(no_below=5, no_above=0.1)
    logger.info('%s words remained after filetering.' %len(word_count_dict))
    bag_of_words_corpus = [word_count_dict.doc2bow(pdoc) for pdoc in processed_docs]
    lda_model = LdaModel(
        mpath,
        corpus=bag_of_words_corpus,
        id2word=word_count_dict,
        num_topics=8)
    return lda_model, word_count_dict

def trainmodel_and_save(mpath, src, dest, fname):
    model, wmap = trainmodel(mpath, os.path.join(src,fname))
    dname = os.path.join(dest,fname)
    if not os.path.exists(dname):
        os.mkdir(dname)
    model.save(os.path.join(dname,fname+'.model'))
    wmap.save(os.path.join(dname,fname+'.wordmap'))
    logger.info('%s finished.' %fname)

if __name__ == '__main__':
    if len(sys.argv)<4:
        print 'usage: ./gen_lda.py <src> <dest> <mallet>'
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    mpath = sys.argv[3]
    if not os.path.exists(dest):
        os.mkdir(dest)
    p = Pool()
    for fname in os.listdir(src):
        if fname.startswith('e'):
            p.apply_async(trainmodel_and_save, args=(mpath, src, dest, fname,))
            # trainmodel_and_save(src, dest, fname)
    p.close()
    p.join()
