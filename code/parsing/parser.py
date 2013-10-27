
import nltk

grammar = nltk.parse_cfg(open("grammar.cfg"))
parser  = nltk.ChartParser(grammar)

def parse(sentence):
    sentence = nltk.word_tokenize(sentence)
    return parser.nbest_parse(sentence)[0]

if __name__ == "__main__":
    print parse("the man saw the dog with the telescope")
