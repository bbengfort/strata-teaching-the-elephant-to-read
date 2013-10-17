import nltk

class Mapper(object):
    
    def __init__(self):
        with open(self.params["excludes"], "r") as excludes:
            self.excludes = set(line.strip() for line in excludes)

    def __call__(self, key, value):
        for word in nltk.word_tokenize(value):
            if not word in self.excludes:
                yield word, 1

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
