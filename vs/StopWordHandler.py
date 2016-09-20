class StopWordHandler(object):

    def __init__(self,path):
        self.__path = path
        self.__wordList = self.__loadFile()

    def __loadFile(self):
        stopwordSet = set()
        with open(self.__path, 'r') as f:
            for line in f.readlines():
                stopwordSet.add(line.strip())
        return stopwordSet

    def exist(self, word):
        return word in self.__wordList

if __name__ == '__main__':
    s = StopWordHandler('stop_words.utf8')
    print s.exist('a')
