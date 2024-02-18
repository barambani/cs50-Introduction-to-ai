from tictactoe import *

def test_terminal_empty_board():
    test_board = [[EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY]]
    expected = False
    assert terminal(test_board) == expected, f'Empty Board - The terminal status should be {expected}'

def test_terminal_1():
    test_board = [[EMPTY, X, EMPTY],
                  [X, X, O],
                  [O, O, EMPTY]]
    expected = False
    assert terminal(test_board) == expected, f'The terminal status should be {expected}'

def test_terminal_2():
    test_board = [[EMPTY, EMPTY, X],
                  [O, X, EMPTY],
                  [X, O, EMPTY]]
    expected = True
    assert terminal(test_board) == expected, f'The terminal status should be {expected}'

def test_terminal_3():
    test_board = [[EMPTY, X, X],
                  [O, O, O],
                  [X, O, X]]
    expected = True
    assert terminal(test_board) == expected, f'The terminal status should be {expected}'

def test_terminal_complete():
    test_board = [[X, O, X],
                  [X, X, O],
                  [O, X, O]]
    expected = True
    assert terminal(test_board) == expected, f'The terminal status should be {expected}'