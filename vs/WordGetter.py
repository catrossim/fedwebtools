import gensim, logging
class WordGetter(object):

    def __init__(self, path):
        logging.info('Loading model from %s' % path)
        self.model = self._load_model(path, binary)
        logging.info('Model is loaded.')

    def _load_model(path, binary):
        return gensim.models.Word2Vec.load(path)

    def most_similar(words, topn=10):
        return self.model.most_similar(positive=words, topn=topn)
