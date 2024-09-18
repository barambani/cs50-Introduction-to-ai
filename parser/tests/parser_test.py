import os

from parser.parser import *

sentences_pat = "./sentences"

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def test(sentence):
    words = preprocess(sentence)
    print(words)
    return list(parser.parse(words))


def nonterminals_test_1():
    print()
    sentences_files = sorted(os.listdir(sentences_pat))
    for file in sentences_files:
        with open(os.path.join(sentences_pat, file)) as f:
            trees = test(f.read())
            assert len(trees) > 0, f'Found: {len(trees)} trees. Should be > 0'


def nonterminals_test_2():
    print()
    sentences = [
        "Holmes sat in the armchair.",
        "Holmes sat in the red armchair.",
        "Holmes sat in the little red armchair.",
        "I had a little moist red paint in the palm of my hand.",
        "Holmes sat down and lit his pipe."
    ]
    for sentence in sentences:
        trees = test(sentence)
        assert len(trees) > 0, f'Found: {len(trees)} trees. Should be > 0'


def nonterminals_test_3():
    print()
    sentences = [
        "Holmes sat in the the armchair."
    ]
    for sentence in sentences:
        trees = test(sentence)
        assert len(trees) == 0, f'Found: {len(trees)} trees. Should be 0'