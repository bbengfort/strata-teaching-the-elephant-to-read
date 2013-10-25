#!/usr/bin/env python

"""
Joins the documents in the NLTK Reuters corpus so that we can do TF-IDF
and other pipeline operations on a unified corpus rather than many, many
small files.

This file joins the internal files into one large file and seperates the
indvidual files with a seperator that contains the document id.
"""

import os

CORPUS_ROOT = '/usr/local/share/nltk_data/corpora/reuters'

def corpus_names(path):
    testdir  = os.path.join(path, 'test')
    traindir = os.path.join(path, 'training')

    for name in os.listdir(testdir):
        yield os.path.join(testdir, name)

    for name in os.listdir(traindir):
        yield os.path.join(traindir, name)

def sepit(path):
    bar = '=' * 34
    name = int(os.path.basename(path))
    return "%s %05d %s\n" % (bar, name, bar)

def writer(inpath, outpath):
    with open(outpath, 'w') as out:
        for path in corpus_names(inpath):
            with open(path, 'r') as f:
                out.write(sepit(path))
                out.write(f.read())

if __name__ == "__main__":
    #writer(CORPUS_ROOT, "reuters.txt")
    print len(list(corpus_names(CORPUS_ROOT)))
