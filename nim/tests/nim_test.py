from nim.nim import *

from hypothesis import given

from . import generators as gen

def get_q_value_test_1():
    ai = NimAI(alpha = 1)
    ai.update_q_value([1, 1, 3, 5], (2, 3), 0, 1, 0)
    result = ai.get_q_value([1, 1, 3, 5], (3, 1))
    expected = 0
    assert result == expected, f'Found: {result}. Should be {expected}'


def get_q_value_test_2():
    ai = NimAI(alpha = 1)
    ai.update_q_value([1, 1, 3, 5], (2, 3), 0, 1, 0)
    result = ai.get_q_value([1, 1, 3, 5], (2, 3))
    expected = 1
    assert result == expected, f'Found: {result}. Should be {expected}'


def best_future_reward_test_1():
    ai = NimAI()
    ai.update_q_value([1, 1, 3, 5], (2, 3), 0, 1, 0)
    ai.update_q_value([3, 0, 4, 7], (0, 2), 0, -1, 0)
    ai.update_q_value([0, 2, 2, 1], (1, 1), 0, 0, 0)
    ai.update_q_value([3, 0, 4, 7], (0, 1), 0, 3, 0)
    ai.update_q_value([3, 0, 4, 7], (3, 4), 0, 1, 0)
    ai.update_q_value([1, 1, 3, 5], (2, 3), 0, 2, 0)
    ai.update_q_value([3, 0, 4, 7], (2, 2), 0, 1, 0)
    result = ai.best_future_reward([3, 0, 4, 7])
    expected = 1.5
    assert result == expected, f'Found: {result}. Should be {expected}'


def best_future_reward_test_2():
    ai = NimAI()
    ai.update_q_value([1, 1, 3, 5], (2, 3), 0, 1, 0)
    ai.update_q_value([3, 0, 4, 7], (0, 2), 0, -1, 0)
    ai.update_q_value([0, 2, 2, 1], (1, 1), 0, 0, 0)
    ai.update_q_value([3, 0, 4, 7], (0, 1), 0, 3, 0)
    ai.update_q_value([3, 0, 4, 7], (3, 4), 0, 1, 0)
    ai.update_q_value([1, 1, 3, 5], (2, 3), 0, 2, 0)
    ai.update_q_value([3, 0, 4, 7], (2, 2), 0, 1, 0)
    result = ai.best_future_reward([5, 0, 4, 7])
    expected = 0
    assert result == expected, f'Found: {result}. Should be {expected}'


@given(state = gen.states(10, 100))
def a_random_action_for_test_1(state):
    ai = NimAI()
    pile, count = ai.a_random_action_for(state)
    assert state[pile] >= count, f'The state {state} can\'t accept the action ({pile,}, {count})'