"""
Quick sentiment analyses with NLTK Naive Bayes classification based on the
NLTK built in Moview Reviews Corpus. This code is from the following post:

http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
"""


import nltk.classify.util

from nltk import wordpunct_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def wordfeature(words):
    """
    Bag of Words model!
    """
    return dict([(word, True) for word in words])

class SentimentModel(object):

    def __init__(self, corpus=None):
        self.corpus = corpus
        self.negids = corpus.fileids('neg')
        self.posids = corpus.fileids('pos')

        self._negfeats   = None
        self._posfeats   = None
        self._classifier = None

    @property
    def negative_features(self):
        if not self._negfeats:
            self._negfeats = [(wordfeature(self.corpus.words(fileids=f)), 'neg')
                              for f in self.negids]
        return self._negfeats

    @property
    def positive_features(self):
        if not self._posfeats:
            self._posfeats = [(wordfeature(self.corpus.words(fileids=f)), 'pos')
                              for f in self.posids]
        return self._posfeats

    def cutoff(self, features):
        return len(features) * 3/4

    @property
    def training(self):
        negcut = self.cutoff(self.negative_features)
        poscut = self.cutoff(self.positive_features)
        return self.negative_features[:negcut] + self.positive_features[:poscut]

    @property
    def test(self):
        negcut = self.cutoff(self.negative_features)
        poscut = self.cutoff(self.positive_features)
        return self.negative_features[negcut:] + self.positive_features[poscut:]

    @property
    def classifier(self):
        if not self._classifier:
            self._classifier = NaiveBayesClassifier.train(self.training)
        return self._classifier

    @property
    def accuracy(self):
        return nltk.classify.util.accuracy(self.classifier, self.test)

    def show_most_informative_features(self):
        return self.classifier.show_most_informative_features()

    def analyze(self, sentence):
        tokens  = wordpunct_tokenize(sentence)
        feature = wordfeature(tokens)
        return self.classifier.classify(feature)

    def __str__(self):
        output = []
        output.append("Trained on %d instances, tested on %d instances")
        output.append("Classifier Accuracy: %0.3f")
        output.append("")
        return "\n".join(output) % (len(self.training), len(self.test), self.accuracy)

if __name__ == "__main__":
    model = SentimentModel(movie_reviews)
    print model
    model.show_most_informative_features()
