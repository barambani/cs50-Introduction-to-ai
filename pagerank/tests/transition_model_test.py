from pagerank.pagerank import *

def transition_model_test_1():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": { "3.html" },
        "3.html": { "2.html" }
    }
    page = "1.html"
    damping_factor = 0.85
    result = transition_model(corpus, page, damping_factor)
    expected = { "1.html": 0.05, "2.html": 0.475, "3.html": 0.475 }
    assert result == expected, f'Found: {result}. Should be {expected}'


def transition_model_test_2():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": { "3.html" },
        "3.html": { "2.html" }
    }
    page = "2.html"
    damping_factor = 0.85
    result = transition_model(corpus, page, damping_factor)
    expected = { "1.html": 0.05, "2.html": 0.05, "3.html": 0.9 }
    assert result == expected, f'Found: {result}. Should be {expected}'


def transition_model_test_3():
    corpus = {
        "1.html": { "2.html", "3.html" },
        "2.html": { "3.html" },
        "3.html": { "2.html" }
    }
    page = "3.html"
    damping_factor = 0.85
    result = transition_model(corpus, page, damping_factor)
    expected = { "1.html": 0.05, "2.html": 0.9, "3.html": 0.05 }
    assert result == expected, f'Found: {result}. Should be {expected}'


def transition_model_test_4():
    corpus = {
        "1.html": { "2.html" },
        "2.html": { "2.html", "1.html" },
    }
    page = "2.html"
    damping_factor = 0.85
    result = transition_model(corpus, page, damping_factor)
    expected = { "1.html": 0.5, "2.html": 0.5 }
    assert result == expected, f'Found: {result}. Should be {expected}'


def transition_model_test_5():
    corpus = {
        "1.html": { "2.html" },
        "2.html": {},
    }
    page = "2.html"
    damping_factor = 0.85
    result = transition_model(corpus, page, damping_factor)
    expected = { "1.html": 0.5, "2.html": 0.5 }
    assert result == expected, f'Found: {result}. Should be {expected}'