import nltk

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

class Mapper(object):

    def __init__(self):
        if 'stopwords' in self.params:
            with open(self.params['stopwords'], 'r') as excludes:
                self._stopwords = set(line.strip() for line in excludes)
        else:
            self._stopwords = None

        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, key, value):
        for word in self.tokenize(value):
            if not word in self.stopwords:
                yield word, 1

    def normalize(self, word):
        word = word.lower()
        return self.lemmatizer.lemmatize(word)

    def tokenize(self, sentence):
        for word in wordpunct_tokenize(sentence):
            yield self.normalize(word)

    @property
    def stopwords(self):
        if not self._stopwords:
            self._stopwords = nltk.corpus.stopwords.words('english')
        return self._stopwords

def reducer(key, values):
    yield key, sum(values)

def runner(job):
    job.additer(Mapper, reducer, reducer)

def starter(prog):
    excludes = prog.delopt("stopwords")
    if excludes: prog.addopt("param", "stopwords="+excludes)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner, starter)
