from pagerank.pagerank import *
from pagerank.tests.test_util import *


def sample_pagerank_test_1():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": { "3.html" },
        "3.html": { "2.html" }
    }
    damping_factor = 0.85
    samples = 100000
    result = sample_pagerank(corpus, damping_factor, samples)
    expected = { "1.html": 0.05, "2.html": 0.475, "3.html": 0.475 }
    assert are_page_ranks_close(result, expected), f'Found: {result}. Should be {expected}'


def sample_pagerank_test_2():
    corpus = {
        "1.html": { "2.html" },
        "2.html": { "2.html", "1.html" },
    }
    damping_factor = 0.85
    samples = 100000
    result = sample_pagerank(corpus, damping_factor, samples)
    expected = { "1.html": 0.35, "2.html": 0.65 }
    assert are_page_ranks_close(result, expected, tol = 0.005), f'Found: {result}. Should be {expected}'


def sample_pagerank_test_3():
    corpus = {
        "1.html": { "2.html" },
        "2.html": {},
    }
    damping_factor = 0.85
    samples = 100000
    result = sample_pagerank(corpus, damping_factor, samples)
    expected = { "1.html": 0.35, "2.html": 0.65 }
    assert are_page_ranks_close(result, expected, tol = 0.005), f'Found: {result}. Should be {expected}'


def sample_pagerank_test_4():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": {},
        "3.html": { "2.html" }
    }
    damping_factor = 0.85
    samples = 100000
    result = sample_pagerank(corpus, damping_factor, samples)
    expected = { "1.html": 0.198, "2.html": 0.521, "3.html": 0.281 }
    assert are_page_ranks_close(result, expected, tol = 0.005), f'Found: {result}. Should be {expected}'