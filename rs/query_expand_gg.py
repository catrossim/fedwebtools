#coding: utf-8
from rs_utils import save
import os, json
def tokenize(post):
    from nltk import word_tokenize, stem
    import string
    from StopWordHandler import StopWordHandler
    stopwords = StopWordHandler('resource/stop_words.utf8')
    post = post.replace(u'\u2014',' ').replace(u'\u2013',' ').replace(u'\xb7','').replace(u'\u2022','')
    if isinstance(post, unicode):
        post = post.encode('utf-8')
    # 转化为小写
    text = post.lower()
    # 移除标点
    no_punctuation = text.translate(None, string.punctuation)
    # 分词
    tokens = word_tokenize(unicode(no_punctuation,'utf-8'))
    # 词干提取
    stemmer = stem.SnowballStemmer('english')
    stem_tokens = [stemmer.stem(x) for x in tokens if not stopwords.exist(x) and not x.isdigit()]
    return stem_tokens

if __name__ == '__main__':
    qdir = 'resource/snippet_google/'
    dest = 'resource/expqs_google'
    if not os.path.exists(dest):
        os.mkdir(dest)
    for f in os.listdir(qdir):
        result = []
        with open(os.path.join(qdir,f)) as data_file:
            data = json.load(data_file)
        for item in data['items']:
            text = item['title']+item['snippet']
            result.extend(tokenize(text))
        count = {}
        for word in result:
            if count.get(word,None):
                count[word] += 1
            else:
                count[word] = 1
        sorted_count = sorted(count.items(),key=lambda d:d[1],reverse=True)
        save(
            os.path.join(dest, f),
            '\n'.join([' '.join(x) for x in map(lambda t:(t[0],str(t[1])),sorted_count)])
        )
