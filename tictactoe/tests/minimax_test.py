from tictactoe.tictactoe import *

def test_minimax_1():
    test_board = [[EMPTY, O, X],
                  [EMPTY, X, EMPTY],
                  [O, EMPTY, EMPTY]]
    expected = (1, 2)
    assert minimax(test_board) == expected, f'The minimax result should be {expected}'


def test_minimax_2():
    test_board = [[EMPTY, O, X],
                  [O, X, X],
                  [O, EMPTY, EMPTY]]
    expected = (2, 2)
    assert minimax(test_board) == expected, f'The minimax result should be {expected}'


def test_minimax_3():
    test_board = [[EMPTY, O, X],
                  [EMPTY, X, X],
                  [O, EMPTY, O]]
    expected = (1, 0)
    assert minimax(test_board) == expected, f'The minimax result should be {expected}'


def test_minimax_4():
    test_board = [[EMPTY, X, O],
                  [O, X, EMPTY],
                  [X, EMPTY, O]]
    expected = (2, 1)
    assert minimax(test_board) == expected, f'The minimax result should be {expected}'


def test_minimax_5():
    test_board = [[EMPTY, X, O],
                  [O, X, X],
                  [X, EMPTY, O]]
    expected = (2, 1)
    assert minimax(test_board) == expected, f'The minimax result should be {expected}'


def test_minimax_6():
    test_board = [[EMPTY, X, X],
                  [O, EMPTY, X],
                  [EMPTY, O, O]]
    expected = (0, 0)
    assert minimax(test_board) == expected, f'The minimax result should be {expected}'