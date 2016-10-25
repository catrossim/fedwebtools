import sys, os
from rs_utils import save, readfilebylines

if __name__ == '__main__':
    src = sys.argv[1]
    # QueryID, Q0 (unused), resourceID, rank, score and runtag
    runtag = sys.argv[2]
    fstr = '{} Q0 {} {} {} {}'
    result = []
    for file in os.listdir(src):
        lines = readfilebylines(os.path.join(src,file))
        rank = 1
        for line in lines:
            token = line.strip().split(' ')
            result.append(
                fstr.format(
                    file,
                    'FW14-'+token[0],
                    rank,
                    token[1],
                    runtag
                    )
                )
            rank += 1
    save(runtag, '\n'.join(result))
