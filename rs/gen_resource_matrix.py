import numpy as np
from sklearn.preprocessing import StandardScaler
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from rs_utils import readfilebylines
import sys
from timeit import Timer

def gen_resource_matrix(model, corpus, wc_dict):
    result = {}
    for doc in corpus:
        r = model.get_document_topics(wc_dict.doc2bow(doc))
        for t in r:
            if result.get(t[0],None):
                result[t[0]].append(t[1])
            else:
                result[t[0]] = [t[1]]
    rsum = {}
    for k,v in result.iteritems():
        rsum[k] = np.array(v).mean()
    x = np.array(rsum.values()).reshape(-1,1)
    return StandardScaler().fit_transform(x).reshape(1,-1)

def tokenize(text):
    return text.strip().split(' ')

def gen_resource_matrix_and_save(model, corpus, wc_dict, output):
    rmatrix = gen_resource_matrix(model, corpus, wc_dict)
    np.save(output, rmatrix)

if __name__ == '__main__':
    if len(sys.argv)<4:
        print 'usage: python gen_resource_matrix.py <corpus_dir> <model_dir> \
            <output_dir>'
        sys.exit(1)
    corpus_dir = sys.argv[1]
    model_dir = sys.argv[2]
    output_dir = sys.argv[3]
    import os
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    from multiprocessing import Pool
    p = Pool()
    for rname in os.listdir(model_dir):
        c_target = os.path.join(corpus_dir, rname)
        m_target = os.path.join(model_dir, rname, rname)
        corpus = [tokenize(c) for c in readfilebylines(c_target)]
        wc_dict = Dictionary.load(m_target+'.wordmap')
        lda_model = LdaModel.load(m_target+'.model')
        p.apply_async(
            gen_resource_matrix_and_save,
            args=(
                lda_model,
                corpus,
                wc_dict,
                os.path.join(output,rname)
            )
        )
    p.close()
    p.join()

    # corpus = [tokenize(c) for c in readfilebylines(corpus_path)]
    # wc_dict = Dictionary(corpus)
    # lda_model = LdaModel.load(model_path)
    # print gen_resource_matrix(lda_model, corpus, wc_dict)
