import math
import string

from itertools import groupby
from operator import itemgetter

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

N = 50.0 # Number of documents, in float to make division work.

class TermMapper(object):

    def __init__(self):
        if 'stopwords' in self.params:
            with open(self.params['stopwords'], 'r') as excludes:
                self._stopwords = set(line.strip() for line in excludes)
        else:
            self._stopwords = None

    def __call__(self, key, value):
        for word in self.tokenize(value):
            if not word in self.stopwords:
                yield (word, key), 1

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
        yield (term, docid), idf

class SumReducer(object):

    def __call__(self, key, values):
        yield key, sum(values)

class BufferReducer(object):

    def __call__(self, key, values):
        term = key
        for docid, group in groupby(values, itemgetter(0)):
            group = list(group)
            tf = group[0][1]
            n  = sum(g[2] for g in group)
            yield (term, docid), (tf, n)

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
