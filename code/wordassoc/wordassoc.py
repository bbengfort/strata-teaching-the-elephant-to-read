"""
Mapper and Reducer based on N. Madnani's PyCon Presentation from:
    http://www.umiacs.umd.edu/~nmadnani/pycon/hwordassoc.py
"""

import re

from nltk import FreqDist
from nltk.corpus import stopwords

_badpattern = re.compile(r'\d|\W|_')

class Mapper(object):

    def __init__(self):
        if 'stopwords' in self.params:
            with open(self.params['stopwords'], 'r') as excludes:
                self._stopwords = set(line.strip() for line in excludes)
        else:
            self._stopwords = None

    def __call__(self, key, value):
        sent = value.split()
        for idx, tagged in enumerate(sent):
            token, tag = self.split_tagged(tagged)

            if self.valid(token, tag):
                dist   = FreqDist()
                window = sent[idx+1:idx+5]

                for wtagged in window:
                    wtoken, wtag = self.split_tagged(wtagged)

                    if self.valid(wtoken, wtag):
                        dist.inc(wtoken)

                yield token, tuple(dist.items())

    @property
    def stopwords(self):
        if not self._stopwords:
            self._stopwords = stopwords.words('english')
        return self._stopwords

    def split_tagged(self, tagged):
        if tagged.count('/') == 1:
            token, tag = tagged.split('/')
            return token.lower(), tag
        return None, None

    def is_noun(self, tag):
        tag = tag.upper()
        return tag.startswith('N')

    def proper_length(self, token):
        return 2 < len(token) <= 20

    def is_clean(self, token):
        return not bool(_badpattern.search(token))

    def valid(self, token, tag):
        return bool(token and self.is_clean(token) and self.proper_length(token)
                    and self.is_noun(tag) and token not in self.stopwords)

class Reducer(object):

    def __call__(self, key, values):
        dist = FreqDist()
        for fd in values:
            for k, v in fd:
                dist.inc(k, v)
        yield key, tuple(dist.items())

def runner(job):
    job.additer(Mapper, Reducer, combiner=Reducer)

def starter(prog):
    excludes = prog.delopt("stopwords")
    if excludes: prog.addopt("param", "stopwords="+excludes)

if __name__ == "__main__":
    import dumbo
    dumbo.main(runner, starter)
