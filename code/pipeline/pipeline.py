from ast import literal_eval
from nltk import sent_tokenize, word_tokenize, pos_tag

class PipelineMapper(object):

    def __init__(self):
        self.lineno = 0

    def __call__(self, key, value):
        for token in self.tokenize(value):
            if token:
                self.lineno += 1
                yield self.lineno, token

    def tokenize(self, value):
        raise NotImplementedError("Subclasses must provide a tokenizer")

class ParagraphMapper(PipelineMapper):

    def __init__(self):
        self.parano  = 0
        self.current = ""

    def __call__(self, key, value):
        value = value.strip()
        if not value:
            if self.current:
                self.parano += 1
                yield self.parano, self.current
                self.current = ""
        self.current += " " + value

class SegmenterMapper(PipelineMapper):

    def tokenize(self, value):
        if not value: yield None
        for sentence in sent_tokenize(value):
            yield sentence

class TokenizeMapper(PipelineMapper):

    def tokenize(self, value):
        if not value: yield None
        yield tuple(word_tokenize(value))

class TaggerMapper(PipelineMapper):

    def tokenize(self, value):
        if not value: yield None
        #value = literal_eval(value)
        yield tuple(pos_tag(value))

class IdentityReducer(object):

    def __call__(self, key, values):
        for value in values:
            yield key, value

def runner(job):
    job.additer(ParagraphMapper, IdentityReducer)
    job.additer(SegmenterMapper, IdentityReducer)
    job.additer(TokenizeMapper, IdentityReducer)
    job.additer(TaggerMapper, IdentityReducer)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner)
