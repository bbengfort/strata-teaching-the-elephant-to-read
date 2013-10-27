from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk import wordpunct_tokenize

def bag_of_words(sentence):
    if isinstance(sentence, basestring):
        sentence = wordpunct_tokenize(sentence)
    return dict([(word, True) for word in sentence])


negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(bag_of_words(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(bag_of_words(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

classifier = NaiveBayesClassifier.train(negfeats + posfeats)

print classifier.classify(bag_of_words("An astounding triumph!"))
print classifier.classify(bag_of_words("The movie was idiotic and ludicrous."))
