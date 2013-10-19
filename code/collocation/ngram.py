import nltk

from nltk.util import bigrams, trigrams
from nltk.tokenize import word_tokenize

class Mapper(object):

    def __call__(self, key, value):
        for ngram in self.trigrams(value):
            yield ngram, 1

    def bigrams(self, value):
        for bigram in bigrams(self.tokenize(value)):
            yield bigram

    def trigrams(self, value):
        for trigram in trigrams(self.tokenize(value)):
            yield trigram

    def normalize(self, word):
        word = word.lower()
        return word

    def tokenize(self, sentence):
        for word in word_tokenize(sentence):
            yield self.normalize(word)

def reducer(key, values):
    yield key, sum(values)

def runner(job):
    job.additer(Mapper, reducer, reducer)

def starter(prog):
    excludes = prog.delopt("excludes")
    if excludes: prog.addopt("param", "excludes="+excludes)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner, starter)
