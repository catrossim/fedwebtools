import numpy as np
import pandas as pd

def f_mk(df):
    df['r_mk'] = np.arange(1,len(df)+1)
    return df

def change_e(df):
    df['e'] = 'FW14-'+df['e']
    return df

def gen_result(src, dest):
    npy_file = np.load(src)
    rdict = npy_file.item()
    reform = {(outkey, inkey): [values] for outkey, innerDict in rdict.iteritems() for inkey, values in innerDict.iteritems()}
    result = pd.DataFrame(reform).T.replace(np.inf,0)
    rtemp = result.reset_index()
    rtemp.rename(columns={0:'score', 'level_0':'q','level_1':'e'},inplace=True)
    rgroup = rtemp.groupby('q')['score']
    re = rtemp.set_index(['q', rtemp.index])
    re = re.ix[rgroup.apply(lambda x:x.sort_values(ascending=False)).index]
    out = re.groupby(level=0).apply(f_mk)
    out = out.reset_index()
    out['Q0'] = 'Q0'
    out['runID'] = 'rs_lda_s'
    del out['level_1']
    out = out.apply(change_e,axis=1)
    out = out.take([0,-2,1,2,3,5],axis=1)
    out.to_csv(dest,header=None,sep=' ',index=False)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage: python gen_rs_lda_s_result.py <src> <dest>'
    src = sys.argv[1]
    dest = sys.argv[2]
    gen_result(src, dest)
