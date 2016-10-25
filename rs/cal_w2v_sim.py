from WordGetter import WordGetter
import sys, os, logging, time
from rs_utils import save,readfilebylines
logger = logging.getLogger('cal_w2v_sim')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def cal_by_words(wl1, wl2):
    sum = 0
    for i1 in xrange(len(wl1)):
        weight1 = 1.0/(i1+1)
        for i2 in xrange(len(wl2)):
            weight2 = 1.0/(i2+1)
            try:
                sim = wgetter.similarity(wl1[i1],wl2[i2])
            except KeyError:
                sim = 0
            sum += sim*weight1*weight2
    return sum

# 7011 vs topn
def cal_sim(query_file, topic_dir):
    base = os.path.basename(query_file)
    qs = [line.split(' ')[0] for line in readfilebylines(query_file)]
    result = {}
    # e001 in topn
    for dir in os.listdir(topic_dir):
        # 0 in e001
        sum = 0
        for file in os.listdir(os.path.join(topic_dir,dir)):
            tws = [line.split(' ')[0] for line in readfilebylines(os.path.join(topic_dir,dir,file))]
            score = cal_by_words(qs, tws)
            sum += score
        result[dir] = sum
    return result

def cal_sim_and_save(query_path, topic_dir, output_dir):
    start = time.time()
    result = cal_sim(query_path, topic_dir)
    basename = os.path.basename(query_path)
    sorted_r = sorted(result.items(), key=lambda x:-1*x[1])
    sorted_r = map(lambda x: (x[0],str(x[1])), sorted_r)
    save(os.path.join(output_dir,basename), '\n'.join([' '.join(x) for x in sorted_r]))
    end = time.time()
    logger.info('{} was finished and took {:.3f}s'.format(basename, end-start))

class TestWGetter(object):
    def __init__(self, **kw):
        print 'TestWGetter'

    def similarity(self, w1, w2):
        return 1.0

if __name__ == '__main__':
    model_file = sys.argv[1]
    query_dir = sys.argv[2]
    topic_dir = sys.argv[3]
    output_dir = sys.argv[4]
    logger.info(
        'model_file:\'{}\', query_dir:\'{}\', topic_dir:\'{}\', output_dir:\'{}\''.format(
            model_file, query_dir, topic_dir, output_dir
        ))
    global wgetter
    # wgetter = WordGetter(model_file)
    wgetter = TestWGetter()
    result = {}
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    start = time.time()
    # for query_file in os.listdir(query_dir):
    #     r = cal_sim_and_save(os.path.join(query_dir,query_file), topic_dir, output_dir)

    from multiprocessing import Pool
    p = Pool()
    for query_file in os.listdir(query_dir):
        p.apply_async(
            cal_sim_and_save,
            args=(
                os.path.join(query_dir,query_file),
                topic_dir,
                output_dir
                )
            )
    p.close()
    p.join()
    end = time.time()
    logger.info('ALL were finished and took {:.3f}s.'.format(end-start))
