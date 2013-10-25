import math
import string

from itertools import groupby
from operator import itemgetter

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

N = 10788.0 # Number of documents, in float to make division work.

class TermMapper(object):

    def __init__(self):
        if 'stopwords' in self.params:
            with open(self.params['stopwords'], 'r') as excludes:
                self._stopwords = set(line.strip() for line in excludes)
        else:
            self._stopwords = None

        self.curdoc = None

    def __call__(self, key, value):
        if value.startswith('='*34):
            self.curdoc = int(value.strip("=").strip())
        else:
            for word in self.tokenize(value):
                if not word in self.stopwords:
                    yield (word, self.curdoc), 1

    def normalize(self, word):
        word = word.lower()
        if word not in string.punctuation:
            return word

    def tokenize(self, sentence):
        for word in wordpunct_tokenize(sentence):
            word = self.normalize(word)
            if word: yield word

    @property
    def stopwords(self):
        if not self._stopwords:
            self._stopwords = stopwords.words('english')
        return self._stopwords

class UnitMapper(object):

    def __call__(self, key, value):
        term, docid = key
        yield term, (docid, value, 1)

class IDFMapper(object):

    def __call__(self, key, value):
        term, docid = key
        tf, n = value
        idf = math.log(N/n)
        yield (term, docid), idf*tf

class SumReducer(object):

    def __call__(self, key, values):
        yield key, sum(values)

class BufferReducer(object):

    def __call__(self, key, values):
        term   = key
        values = list(values)
        n = sum(g[2] for g in values)
        for g in values:
            yield (term, g[0]), (g[1], n)

class IdentityReducer(object):

    def __call__(self, key, values):
        for value in values:
            yield key, value

def runner(job):
    job.additer(TermMapper, SumReducer, combiner=SumReducer)
    job.additer(UnitMapper, BufferReducer)
    job.additer(IDFMapper, IdentityReducer)

def starter(prog):
    excludes = prog.delopt("stopwords")
    if excludes: prog.addopt("param", "stopwords="+excludes)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner, starter)
