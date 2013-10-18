import nltk

class Mapper(object):
    
    def __init__(self):
        if 'stopwords' in self.params:
            with open(self.params['stopwords'], 'r') as excludes:
                self._stopwords = set(line.strip() for line in excludes)
        else:
            self._stopwords = None

    def __call__(self, key, value):
        for word in nltk.word_tokenize(value):
            if not word in self.stopwords:
                yield word, 1

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
    excludes = prog.delopt("excludes")
    if excludes: prog.addopt("param", "excludes="+excludes)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner, starter)
