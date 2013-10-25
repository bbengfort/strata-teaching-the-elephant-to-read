from __future__ import division
from nltk.tokenize import wordpunct_tokenize

class VocabularyMapper(object):

    def __call__(self, key, value):
        for word in self.tokenize(value):
                yield word, 1

    def normalize(self, word):
        return word.lower()

    def tokenize(self, sentence):
        for word in wordpunct_tokenize(sentence):
            yield self.normalize(word)

class LexicalDiversityReducer(object):

    def __init__(self):
        self.vocab  = 0
        self.tokens = 0

    def __call__(self, key, values):
        self.vocab += 1
        self.tokens += sum(values)
        lexdiv = self.tokens / self.vocab
        yield self.vocab, self.tokens, lexdiv

def runner(job):
    job.additer(VocabularyMapper, LexicalDiversityReducer)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner)
