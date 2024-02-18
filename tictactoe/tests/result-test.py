import pytest

from tictactoe import *

def test_result_empty_board():
    test_board = [[EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY]]
    test_move = (2, 2)
    expected = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
    assert result(test_board, test_move) == expected, f'Empty Board - The result should be {expected}'


def test_result_1():
    test_board = [[EMPTY, X, EMPTY],
                  [X, X, O],
                  [O, O, EMPTY]]
    test_move = (3, 3)
    expected = [[EMPTY, X, EMPTY],
                [X, X, O],
                [O, O, X]]
    assert result(test_board, test_move) == expected, f'The result should be {expected}'


def test_result_invalid_1():
    test_board = [[EMPTY, EMPTY, X],
                  [O, X, EMPTY],
                  [X, O, EMPTY]]
    test_move = (5, 6)
    with pytest.raises(ValueError('Invalid Action')):
        result(test_board, test_move)


def test_result_invalid_2():
    test_board = [[EMPTY, EMPTY, X],
                  [O, X, EMPTY],
                  [X, O, EMPTY]]
    test_move = (2, 1)
    with pytest.raises(ValueError('Invalid Action')):
        result(test_board, test_move)


def test_result_complete_1():
    test_board = [[EMPTY, EMPTY, X],
                  [O, X, EMPTY],
                  [X, O, EMPTY]]
    test_move = (2, 2)
    expected = test_board
    assert result(test_board, test_move) == expected, f'The result should be {expected}'


def test_result_complete_2():
    test_board = [[X, O, X],
                  [X, X, O],
                  [O, X, O]]
    test_move = (3, 3)
    expected = test_board
    assert result(test_board, test_move) == expected, f'The result should be {expected}'