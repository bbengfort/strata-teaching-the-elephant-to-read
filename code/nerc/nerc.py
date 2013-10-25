from ast import literal_eval
from nltk import ne_chunk

class Mapper(object):

    def __call__(self, key, value):
        """
        Expects preproccessed text
        """
        line, value = value.split('\t')
        value = literal_eval(value)
        for token in ne_chunk(value):
            if isinstance(token, tuple):
                continue
            yield str(token), 1

def reducer(key, values):
    yield key, sum(values)

def runner(job):
    job.additer(Mapper, reducer, reducer)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner)
