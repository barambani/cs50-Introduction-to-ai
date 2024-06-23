from crossword.crossword import *
from crossword.generate import *


def enforce_node_consistency_test_1():
    crossword = Crossword("./data/structure0.txt", "./data/words0.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    result = sorted(list(creator.domains.values()), key = lambda x: len(list(x)[0]))
    expected = [
        {'TWO', 'ONE', 'SIX', 'TEN'},
        {'FIVE', 'NINE', 'FOUR'},
        {'FIVE', 'NINE', 'FOUR'},
        {'EIGHT', 'SEVEN', 'THREE'}
    ]
    assert result == expected, f'Found: {result}. Should be {expected}'


def enforce_node_consistency_test_2():
    crossword = Crossword("./data/structure1.txt", "./data/words1.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    result = sorted(list(creator.domains.values()), key = lambda x: len(list(x)[0]))
    expected = [
        {'TRUTH', 'ALPHA', 'FALSE', 'INFER', 'START', 'LOGIC', 'PRUNE', 'GRAPH', 'BAYES', 'DEPTH'},
        {'TRUTH', 'ALPHA', 'FALSE', 'INFER', 'START', 'LOGIC', 'PRUNE', 'GRAPH', 'BAYES', 'DEPTH'},
        {'CREATE', 'MARKOV', 'NEURAL', 'REASON', 'SEARCH'},
        {'RESOLVE', 'MINIMAX', 'NETWORK', 'BREADTH', 'INITIAL'},
        {'RESOLVE', 'MINIMAX', 'NETWORK', 'BREADTH', 'INITIAL'},
        {'SATISFACTION', 'DISTRIBUTION', 'OPTIMIZATION', 'INTELLIGENCE'}
    ]
    assert result == expected, f'Found: {result}. Should be {expected}'


def revise_test_1():
    crossword = Crossword("./data/structure0.txt", "./data/words0.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    sorted_variables = sorted(list(crossword.variables), key = lambda x: x.__str__())
    creator.revise(sorted_variables[1], sorted_variables[3])
    result = sorted(list(creator.domains.values()), key = lambda x: len(list(x)[0]))
    expected = [
        {'TWO', 'ONE', 'SIX', 'TEN'},
        {'FIVE', 'NINE', 'FOUR'},
        {'FIVE', 'NINE', 'FOUR'},
        {'SEVEN'}
    ]
    assert result == expected, f'Found: {result}. Should be {expected}'


def ac3_test_1():
    crossword = Crossword("./data/structure0.txt", "./data/words0.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    result = sorted(
        list(creator.domains.values()),
        key = lambda x: (len(list(x)[0]), len(list(x)), list(x)[0]) if len(list(x)) > 0 else 0
    )
    expected = [
        {'SIX'},
        {'NINE'},
        {'FIVE', 'NINE'},
        {'SEVEN'}
    ]
    assert result == expected, f'Found: {result}. Should be {expected}'


def ac3_test_2():
    crossword = Crossword("./data/structure1.txt", "./data/words1.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    result = sorted(
        list(creator.domains.values()),
        key = lambda x: (len(list(x)[0]), len(list(x)), list(x)[0]) if len(list(x)) > 0 else 0
    )
    expected = [
        {'INFER'},
        {'LOGIC'},
        {'REASON', 'SEARCH'},
        {'MINIMAX'},
        {'RESOLVE', 'NETWORK'},
        {'INTELLIGENCE'}
    ]
    assert result == expected, f'Found: {result}. Should be {expected}'


def consistent_test_1():
    crossword = Crossword("./data/structure1.txt", "./data/words1.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    assignment = {
        Variable(2, 1, 'across', 12): "distribution",
        Variable(1, 7, 'down', 7): "minimax"
    }
    result = creator.consistent(assignment)
    expected = False
    assert result == expected, f'Found: {result}. Should be {expected}'


def consistent_test_2():
    crossword = Crossword("./data/structure1.txt", "./data/words1.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    assignment = {
        Variable(2, 1, 'across', 12): "intelligence",
        Variable(1, 7, 'down', 7): "minimax"
    }
    result = creator.consistent(assignment)
    expected = True
    assert result == expected, f'Found: {result}. Should be {expected}'


def consistent_test_3():
    crossword = Crossword("./data/structure1.txt", "./data/words1.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    assignment = {
        Variable(1, 7, 'down', 7): "minimax",
        Variable(1, 12, 'down', 7): "minimax",
    }
    result = creator.consistent(assignment)
    expected = False
    assert result == expected, f'Found: {result}. Should be {expected}'


def select_unassigned_variable_test_1():
    crossword = Crossword("./data/structure1.txt", "./data/words1.txt")
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()
    creator.ac3()
    assignment = {
        Variable(2, 1, 'across', 12): "intelligence",
    }
    result = creator.select_unassigned_variable(assignment)
    expected = Variable(1, 7, 'down', 7)
    assert result == expected, f'Found: {result}. Should be {expected}'