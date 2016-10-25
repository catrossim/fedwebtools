import gensim, logging
class WordGetter(object):

    def __init__(self, path):
        logging.info('Loading model from %s' % path)
        self.model = self._load_model(path)
        logging.info('Model is loaded.')

    def _load_model(self, path):
        return gensim.models.Word2Vec.load(path)

    def most_similar(self, words, topn=10):
        return self.model.most_similar(positive=words, topn=topn)

    def similarity(self, a, b):
        return self.model.similarity(a, b)
