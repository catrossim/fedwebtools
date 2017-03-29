#!/bin/bash
from rs_utils import readfilebylines, save
import os,sys
from scipy.stats import entropy
import numpy as np
def cal_sim(qmat, rmat):
    return entropy(qmat, rmat)

import pandas as pd
if __name__ == '__main__':
    if len(sys.argv)<6:
        print 'usage: python %s <qorigin> <qmat_dir> <rmat_dir> <dest> <runID>'%sys.argv[0]
        sys.exit()
    qsequence = {}
    count = 0
    qorigin = sys.argv[1]
    qmat_dir = sys.argv[2]
    rmat_dir = sys.argv[3]
    dest = sys.argv[4]
    runID = sys.argv[5]
    for qname in os.listdir(qorigin):
        qsequence[count] = qname
        count += 1
    qmats = {}
    for e in os.listdir(qmat_dir):
        s = pd.read_csv(
            os.path.join(
                qmat_dir,
                e,
                'expqs_google_inf.model-final.theta'
            ),
            header=None,sep=' '
        )
        del s[10]
        qmats[e] = s
    rmats = {}
    for r in os.listdir(rmat_dir):
        rmat = np.load(os.path.join(rmat_dir,r,r+'.npy'))
        print r
        rmats[r] = rmat
    result = {}
    for k,v in qsequence.iteritems():
        qresult = {}
        for qk,qv in qmats.iteritems():
            qmat = qv.iloc[k].tolist()
            rmat = rmats[qk][0].tolist()
            score = cal_sim(qmat,rmat)
            qresult[qk] = score
        result[k] = qresult
#     print result
    out_seq = '%s Q0 FW14-%s %s %s %s'
    out_result = []
    for k,v in result.iteritems():
        q = qsequence[k]
        sorted_e = sorted(v.items(),key=lambda d:d[1],reverse=True)
        rank = 1
        for ek,ev in sorted_e:
            out_result.append(out_seq%(q, ek, rank, ev, runID))
            rank += 1
    save(os.path.join('resource',runID),'\n'.join(out_result))
