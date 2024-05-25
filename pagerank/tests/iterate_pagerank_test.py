from pagerank.pagerank import *
from pagerank.tests.test_util import *


def get_linking_pages_corpus_test_1():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": { "3.html" },
        "3.html": { "2.html" }
    }
    result = get_linking_pages_corpus(corpus)
    expected = {
        "1.html": {},
        "2.html": { "1.html", "3.html" },
        "3.html": { "1.html", "2.html" }
    }
    assert result == expected, f'Found: {result}. Should be {expected}'


def get_linking_pages_corpus_test_2():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": {},
        "3.html": { "2.html" }
    }
    result = get_linking_pages_corpus(corpus)
    expected = {
        "1.html": { "2.html" },
        "2.html": { "1.html", "2.html", "3.html" },
        "3.html": { "1.html", "2.html" }
    }
    assert result == expected, f'Found: {result}. Should be {expected}'


def get_linking_pages_corpus_test_3():
    corpus = {
        "1": {"2"},
        "2": {"1", "3"},
        "3": {"4", "2", "5"},
        "4": {"2", "1"},
        "5": {}
    }
    result = get_linking_pages_corpus(corpus)
    expected = {
        "1": {"2", "4", "5"},
        "2": {"1", "3", "4", "5"},
        "3": {"2", "5"},
        "4": {"3", "5"},
        "5": {"3", "5"}
    }
    assert result == expected, f'Found: {result}. Should be {expected}'


def iterate_pagerank_test_1():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": { "3.html" },
        "3.html": { "2.html" }
    }
    damping_factor = 0.85
    result = iterate_pagerank(corpus, damping_factor)
    expected = { "1.html": 0.05, "2.html": 0.475, "3.html": 0.475 }
    assert are_page_ranks_close(result, expected), f'Found: {result}. Should be {expected}'


def iterate_pagerank_test_2():
    corpus = {
        "1": {"2"},
        "2": {"1", "3"},
        "3": {"4", "2", "5"},
        "4": {"2", "1"},
        "5": {}
    }
    damping_factor = 0.85
    result = iterate_pagerank(corpus, damping_factor)
    expected = { "1": 0.24, "2": 0.35, "3": 0.197, "4": 0.1, "5": 0.1 }
    assert are_page_ranks_close(result, expected, tol = 0.005), f'Found: {result}. Should be {expected}'