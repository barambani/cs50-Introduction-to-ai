from tictactoe.tictactoe import *

def test_winner_empty_board():
    test_board = [[EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY]]
    expected = None
    assert winner(test_board) == expected, f'Empty Board - The winner should be {expected}'

def test_winner_1():
    test_board = [[EMPTY, X, EMPTY],
                  [X, X, O],
                  [O, O, EMPTY]]
    expected = None
    assert winner(test_board) == expected, f'The winner should be {expected}'

def test_winner_2():
    test_board = [[EMPTY, EMPTY, X],
                  [O, X, EMPTY],
                  [X, O, EMPTY]]
    expected = X
    assert winner(test_board) == expected, f'The winner should be {expected}'

def test_winner_3():
    test_board = [[EMPTY, X, X],
                  [O, O, O],
                  [X, O, X]]
    expected = O
    assert winner(test_board) == expected, f'The winner should be {expected}'

def test_winner_4():
    test_board = [[EMPTY, X, O],
                  [EMPTY, EMPTY, O],
                  [X, X, O]]
    expected = O
    assert winner(test_board) == expected, f'The winner should be {expected}'

def test_winner_5():
    test_board = [[EMPTY, X, O],
                  [EMPTY, O, EMPTY],
                  [O, X, X]]
    expected = O
    assert winner(test_board) == expected, f'The winner should be {expected}'

def test_winner_complete():
    test_board = [[X, O, X],
                  [X, X, O],
                  [O, X, O]]
    expected = None
    assert winner(test_board) == expected, f'The winner should be {expected}'