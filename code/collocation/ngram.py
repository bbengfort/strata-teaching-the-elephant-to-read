import nltk
import string

from nltk.util import bigrams, trigrams
from nltk.tokenize import wordpunct_tokenize
from dumbo import MultiMapper, sumreducer, main

class CollocationMapper(object):

    def __call__(self, key, value):
        for ngram in self.ngrams(value):
            yield ngram, 1

    def normalize(self, word):
        word = word.lower()
        return word

    def tokenize(self, sentence):
        for word in wordpunct_tokenize(sentence):
            token = self.normalize(word)
            if token: yield token

    def ngrams(self, value):
        raise NotImplementedError("Subclasses must implement.")

class BigramMapper(CollocationMapper):

    def ngrams(self, value):
        for bigram in bigrams(self.tokenize(value)):
            yield bigram

class TrigramMapper(CollocationMapper):

    def ngrams(self, value):
        for trigram in trigrams(self.tokenize(value)):
            yield trigram

def runner(job):
    mapper = BigramMapper()
    #mapper = TrigramMapper()
    job.additer(mapper, sumreducer, combiner=sumreducer)

if __name__ == "__main__":
    main(runner)
