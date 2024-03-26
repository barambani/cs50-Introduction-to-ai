from minesweeper import *

from hypothesis import given

from tests import strategies as my_st


@given(mines = my_st.cells(10, 10), moves_made = my_st.cells(10, 10))
def make_random_move_test_1(mines, moves_made):
    ai = MinesweeperAI(10, 10)
    ai.mines = mines
    ai.moves_made = moves_made - mines
    result = ai.make_random_move()
    assert result not in ai.mines, f'New random moves shouldn\'t be a mine. Move: {result}. Mines: {ai.mines}'
    assert result not in ai.moves_made, f'New random moves shouldn\'t be already made. Move: {result}. Already made: {ai.moves_made}'


def make_random_move_test_2():
    ai = MinesweeperAI(4, 4)
    ai.knowledge = [
        Sentence([(0, 1), (1, 1)], 1),
        Sentence([(1, 2), (0, 2)], 1),
        Sentence([(1, 2), (1, 1)], 1)
    ]
    ai.mines = set([(2, 0), (2, 3)])
    ai.moves_made = set([(0, 0), (1, 0), (3, 0), (2, 1), (3, 1), (2, 2), (3, 2), (0, 3), (1, 3), (3, 3)])
    result = ai.make_random_move()
    expected = [(0, 1), (0, 2)]
    assert result in expected, f'Found: {result}. Should be {expected}'


def neighbours_of_test_1():
    ai = MinesweeperAI(3, 3)
    result = ai.neighbours_of((0, 0))
    expected = set([(0, 1), (1, 0), (1, 1)])
    assert result == expected, f'Found: {result}. Should be {expected}'


def neighbours_of_test_2():
    ai = MinesweeperAI(3, 3)
    result = ai.neighbours_of((1, 2))
    expected = set([(0, 1), (0, 2), (1, 1), (2, 1), (2, 2)])
    assert result == expected, f'Found: {result}. Should be {expected}'


def infer_new_knowledge_test_1():
    ai = MinesweeperAI(3, 3)
    ai.knowledge.append(
        Sentence([(1, 0), (1, 1), (1, 2)], 1)
    )
    ai.knowledge.append(
        Sentence([(2, 0), (1, 0), (1, 1), (1, 2), (2, 2)], 2)
    )
    result = ai.infer_new_knowledge()
    expected = sorted([
        Sentence([(1, 0), (1, 1), (1, 2)], 1),
        Sentence([(2, 0), (2, 2)], 1),
        Sentence([(2, 0), (1, 0), (1, 1), (1, 2), (2, 2)], 2)
    ])
    assert result == expected, f'Found: {result}. Should be {expected}'


def infer_new_knowledge_test_2():
    ai = MinesweeperAI(3, 3)
    ai.knowledge.append(
        Sentence(ai.neighbours_of((0, 2)), 0)
    )
    result = ai.infer_new_knowledge()
    expected = [
        Sentence(ai.neighbours_of((0, 2)), 0)
    ]
    assert result == expected, f'Found: {result}. Should be {expected}'


def infer_new_knowledge_test_3():
    ai = MinesweeperAI(3, 3)
    ai.add_knowledge((0, 2), 0)
    result = sorted(ai.safes - ai.moves_made)
    expected = sorted([(0, 1), (1, 1), (1, 2)])
    assert result == expected, f'Found: {result}. Should be {expected}'


def make_safe_move_test_1():
    ai = MinesweeperAI(3, 3)
    ai.add_knowledge((0, 2), 0)
    result = ai.make_safe_move()
    expected = [(0, 1), (1, 1), (1, 2)]
    assert result in expected, f'Found: {result}. Should be {expected}'