from tictactoe import *

def test_player_empty_board():
    test_board = [[EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY]]
    expected = X
    assert player(test_board) == expected, f'Empty Board - The next player should be {expected}'

def test_player_1():
    test_board = [[EMPTY, EMPTY, EMPTY],
                  [X, X, EMPTY],
                  [O, EMPTY, EMPTY]]
    expected = O
    assert player(test_board) == expected, f'The next player should be {expected}'

def test_player_2():
    test_board = [[X, EMPTY, EMPTY],
                  [X, X, O],
                  [O, EMPTY, O]]
    expected = X
    assert player(test_board) == expected, f'The next player should be {expected}'

def test_player_complete():
    test_board = [[X, O, X],
                  [X, X, O],
                  [O, X, O]]
    expected = O
    assert player(test_board) == expected, f'The next player should be {expected}'    