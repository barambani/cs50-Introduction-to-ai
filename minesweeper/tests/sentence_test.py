from minesweeper import *

def known_mines_test_1():
    cells = [(0, 0), (0, 1)]
    mines = 2
    result = Sentence(cells, mines).known_mines()
    expected = set(cells)
    assert result == expected, f'Found: {result}. Should be {expected}'


def known_mines_test_2():
    cells = [(0, 0), (0, 1), (1, 0)]
    mines = 2
    result = Sentence(cells, mines).known_mines()
    expected = set()
    assert result == expected, f'Found: {result}. Should be {expected}'


def known_safes_test_1():
    cells = [(0, 0), (0, 1), (0, 2)]
    mines = 0
    result = Sentence(cells, mines).known_safes()
    expected = set(cells)
    assert result == expected, f'Found: {result}. Should be {expected}'


def known_safes_test_2():
    cells = [(0, 0), (0, 1), (0, 2)]
    mines = 2
    result = Sentence(cells, mines).known_safes()
    expected = set()
    assert result == expected, f'Found: {result}. Should be {expected}'


def mark_mine_test_1():
    sentence = Sentence([(0, 0), (0, 1), (0, 2)], 2)
    sentence.mark_mine((0, 1))
    result = sentence
    expected = Sentence([(0, 0), (0, 2)], 1)
    assert result == expected, f'Found: {result}. Should be {expected}'


def mark_mine_test_2():
    sentence = Sentence([(0, 0), (0, 1), (1, 0)], 2)
    sentence.mark_mine((2, 2))
    result = sentence
    expected = Sentence([(0, 0), (0, 1), (1, 0)], 2)
    assert result == expected, f'Found: {result}. Should be {expected}'


def mark_mine_test_2():
    sentence = Sentence([(0, 0), (0, 1), (1, 0)], 0)
    sentence.mark_mine((0, 0))
    result = sentence
    expected = Sentence([(0, 1), (1, 0)], 0)
    assert result == expected, f'Found: {result}. Should be {expected}'


def mark_safe_test_1():
    sentence = Sentence([(0, 0), (0, 1), (0, 2)], 2)
    sentence.mark_safe((0, 1))
    result = sentence
    expected = Sentence([(0, 0), (0, 2)], 2)
    assert result == expected, f'Found: {result}. Should be {expected}'


def mark_safe_test_2():
    sentence = Sentence([(0, 0), (0, 1), (0, 2)], 3)
    sentence.mark_safe((0, 1))
    result = sentence
    expected = Sentence([(0, 0), (0, 2)], 2)
    assert result == expected, f'Found: {result}. Should be {expected}'