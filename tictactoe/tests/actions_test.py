from tictactoe import *

def test_actions_empty_board():
    test_board = [[EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY]]
    expected = ALL_ACTIONS
    assert actions(test_board) == expected, f'Empty Board - The actions should be {expected}'

def test_actions_1():
    test_board = [[EMPTY, X, EMPTY],
                  [X, X, O],
                  [O, O, EMPTY]]
    expected = {(0,0), (0, 2), (2, 2)}
    assert actions(test_board) == expected, f'The actions should be {expected}'

def test_actions_2():
    test_board = [[EMPTY, EMPTY, X],
                  [O, X, EMPTY],
                  [X, O, EMPTY]]
    expected = set()
    assert actions(test_board) == expected, f'The actions should be {expected}'

def test_actions_3():
    test_board = [[EMPTY, X, X],
                  [O, O, O],
                  [X, O, X]]
    expected = expected = set()
    assert actions(test_board) == expected, f'The actions should be {expected}'

def test_actions_4():
    test_board = [[EMPTY, X, O],
                  [EMPTY, EMPTY, O],
                  [X, X, O]]
    expected = expected = set()
    assert actions(test_board) == expected, f'The actions should be {expected}'

def test_actions_5():
    test_board = [[EMPTY, X, O],
                  [EMPTY, EMPTY, EMPTY],
                  [X, X, O]]
    expected = expected = {(0,0), (1,0), (1,1), (1,2)}
    assert actions(test_board) == expected, f'The actions should be {expected}'

def test_actions_complete():
    test_board = [[X, O, X],
                  [X, X, O],
                  [O, X, O]]
    expected = set()
    assert actions(test_board) == expected, f'The actions should be {expected}'