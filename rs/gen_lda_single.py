from gen_lda import trainmodel
import sys, os
if __name__ == '__main__':
    if len(sys.argv)<3:
        print 'usage: ./gen_lda_single.py <src file> <dest dir>'
    path = sys.argv[1]
    dest = sys.argv[2]
    model, wmap = trainmodel(path)
    fname = os.path.basename(path)
    dname = os.path.join(dest,fname)
    print dname
    if not os.path.exists(dname):
        os.mkdir(dname)
    model.save(os.path.join(dname, fname+'.model'))
    wmap.save(os.path.join(dname, fname+'.wordmap'))
