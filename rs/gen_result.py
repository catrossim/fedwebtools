import sys, os
from rs_utils import save, readfilebylines

GENERAL_RESOURCE = 'e200'
QUESTION_WORDS = ['what','when','how','where']
qterms = {}

def readQTerms(path):
    for line in readfilebylines(path):
        tokens = line.split('\t')
        qterms[tokens[0]] = tokens[1]

def findQWords(name):
    for w in QUESTION_WORDS:
        if qterms.get(name).find(w)>=0:
            return True
    return False

if __name__ == '__main__':
    src = sys.argv[1]
    # QueryID, Q0 (unused), resourceID, rank, score and runtag
    runtag = sys.argv[2]
    fstr = '{} Q0 {} {} {} {}'
    result = []
    for file in os.listdir(src):
        rank = 1
        lines = readfilebylines(os.path.join(src,file))
        for line in lines:
            token = line.strip().split(' ')
            result.append(fstr.format(file, 'FW14-'+token[0], rank, token[1], runtag))
            rank += 1
    save(runtag, '\n'.join(result))
