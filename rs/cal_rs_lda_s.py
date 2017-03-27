import numpy as np
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from sklearn.preprocessing import StandardScaler
from rs_utils import readfilebylines
import os, sys

def get_query_matrix(query_list, model, wc_dict):
    topics = model.get_document_topics(
        wc_dict.doc2bow(query_list),
        minimum_probability=0
    )
    tarray = []
    for t in topics:
        tarray.append(t[1])
    # x = np.array(tarray).reshape(-1,1)
    # query_v = StandardScaler().fit_transform(x)
    # return query_v.reshape(1,-1)
    return np.array(tarray)

def get_resource_matrix(rpath):
    return np.load(rpath)

def init_models(mdir, rmat_dir):
    rlist = []
    models = {}
    wordmap = {}
    rmatrixes = {}
    for rname in os.listdir(mdir):
        target = os.path.join(mdir,rname,rname)
        rlist.append(rname)
        models[rname] = LdaModel.load(target+'.model')
        wordmap[rname] = Dictionary.load(target+'.wordmap')
        rmatrixes[rname] = np.load(os.path.join(rmat_dir, rname+'.npy'))
    return rlist, models, wordmap, rmatrixes

def cal_sim(qmat, rmat):
    from scipy.stats import entropy
    # KL-Divewrgence
    return entropy(qmat.tolist(),rmat.tolist())
    # from numpy import linalg
    # from math import exp
    # qmat = np.mat(qmat)
    # rmat = np.mat(rmat)
    # num = float(qmat*rmat.T)
    # denom = linalg.norm(qmat)*linalg.norm(rmat)
    # if denom < 1e-6:
    #     return -1
    # return num/denom

if __name__ == '__main__':
    if len(sys.argv)<6:
        print 'usage: python cal_rs_lda_s.py <query_dir> <lda_models_dir>'+\
        ' <rmatrix_dir> <output_dir> <filename>'
        sys.exit(1)
    qdir = sys.argv[1]
    mdir = sys.argv[2]
    rmat_dir = sys.argv[3]
    out_dir = sys.argv[4]
    fname = sys.argv[5]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    rlist, models, wordmap, rmatrixes = init_models(mdir, rmat_dir)
    result = {}
    for qfile in os.listdir(qdir):
        qs = [line.split(' ')[0] for line in readfilebylines(os.path.join(qdir, qfile))]
        qresult = {}
        for r in rlist:
            qmatrix = get_query_matrix(qs, models[r], wordmap[r])
            rmatrix = rmatrixes[r]
            qresult[r] = cal_sim(qmatrix, rmatrix)
        result[qfile] = qresult
    np.save(os.path.join(out_dir, fname), result)
