from ast import literal_eval
from nltk import ConditionalFreqDist

class Generator(object):

    def __init__(self, output, length=15):
        self.output  =  output
        self.length  = length

        self._cfdist = None

    @property
    def cfdist(self):
        if not self._cfdist:
            self._cfdist = ConditionalFreqDist()
            for ngram, count in self.ngrams():
                self._cfdist[ngram[0]].inc(ngram[1], count)
        return self._cfdist

    def ngrams(self):
        with open(self.output, 'r') as output:
            for line in output:
                line = line.strip()
                ngram, count = line.split('\t')
                yield literal_eval(ngram), int(count)

    def generate_iter(self, start, length=None):
        length = length or self.length
        for i in xrange(length):
            yield start
            start = self.cfdist[start].max()

    def generate(self, start, length=None):
        return " ".join(self.generate_iter(start, length))

if __name__ == "__main__":
    g = Generator("output.txt")
    print g.generate("will")
