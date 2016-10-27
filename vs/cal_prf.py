from codecs import open as open
import sys
if __name__ == '__main__':
    file = sys.argv[1]
    c = []
    with open(file,'r','utf-8') as f:
        c = f.readlines()
    sump = 0.0
    sumr = 0.0
    sumf = 0.0
    for line in c:
        tokens = line.split(',')
        sump += float(tokens[1])
        sumr += float(tokens[2])
        sumf += float(tokens[3])
    l = len(c)
    print 'P:{}, R:{}, F1:{}'.format(sump/l,sumr/l,sumf/l)
