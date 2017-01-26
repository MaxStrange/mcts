"""
This is the code for the UCT (Upper Confidence Bounds for Trees)
algorithm.
"""

from ai.node import Node
import copy
import math
import random
from time import process_time


def get_best_move(cur_state, reward_function):
    """
    Gets the AI's best move. Or at least, gets what it thinks is its
    best move.
    The reward_runction parameter is a function that evaluates a terminal
    board position (a game-over gamestate) and returns a value in the interval
    [0, 1], where lower values indicate a bad outcome for the AI, and higher
    values indicated a good outcome for the AI.
    Note that this function is only ever evaluated on TERMINAL game states,
    so it is fine if it is undefined for non-terminal game states.
    """
    return _uct_search(cur_state, reward_function)


def _uct_search(game_state, reward_function):
    root = Node(game_state)
    root.name = "root"

    best_child_of_root = _search_helper(root, reward_function)
    while _child_is_not_most_visited(best_child_of_root, root):
        best_child_of_root = _search_helper(root, reward_function)

    # You would now have a best_child_of_root that is really the
    # most likely child to occur. At this point, that child is of
    # low resolution attack/defend orders, but it would need
    # to somehow resolve these into actual orders,
    # then it should optimize its own orders according to the now
    # 'perfect' information it has of the next move (i.e., what it
    # believes everyone else is going to do)
    # Probably it would be best if it actually gets the top two or three
    # most likely next game states rather than simply one,
    # and then it should choose orders that work best against both
    # (or all three) of these possibilities.
    best_move = best_child_of_root.move_that_derived_this_node()
    return best_move


def _search_helper(root, reward_function):
    start_time = process_time()
    while _within_computational_budget(start_time):
        v = _tree_policy(root)
        delta = _default_policy(v.state, reward_function)
        _back_up(v, delta)
    best_child_of_root = _best_child(root, 0)
    return best_child_of_root


def _child_is_not_most_visited(child, root):
    children = root.children
    for c in children:
        if c is not child:
            if c.num_times_visited > child.num_times_visited:
                return True
    return False



def _back_up(v, delta):
    """
    Give delta to each node in the visit from the newly added node v
    to the root.
    Delta is the value of the terminal node that we reached through v.
    """
    while v is not None:
        # num_times_visited is N in the algorithm
        # total_reward is Q, the total reward of all payouts so far pased
        # through this state
        v.num_times_visited += 1
        v.total_reward += _delta_function(delta, v)
        v = v.parent


def _best_child(v, c):
    # This function should never be called on a node that has no children
    assert(len(v.children) != 0)

    def valfunc(v_prime, v):
        left = v_prime.total_reward / v_prime.num_times_visited
        right = c * math.sqrt((2 * math.log(v.num_times_visited))\
                / v_prime.num_times_visited)
        return left + right
    values_and_nodes = [(valfunc(v_prime, v), v_prime) for v_prime\
            in v.children]
    max_tup = max(values_and_nodes, key=lambda tup: tup[0])

    #if c is 0:
    #    print("Scanning for best move.......")
    #    for v_and_n in values_and_nodes:
    #        print("Node value and num_times_visited: ", str((v_and_n[0], v_and_n[1].num_times_visited)))
    #    print("Decided best move's value is: ", str(max_tup[0]))

    for tup in values_and_nodes:
        if tup == max_tup:
            return tup[1]

    # This should never be reached
    assert(False)


def _default_policy(game_state, reward_function):
    while not game_state.game_over():
        # This function should be replaced with the policy network
        action = random.choice(game_state.possible_moves())
        game_state = copy.deepcopy(game_state)
        game_state.take_turn(action)
    # IMPORTANT: The reward function would need to return a value close to 1
    # for terminal game states that maximize ALL PLAYERS' victories, otherwise
    # uct will keep returning game states where it does something smart while
    # everyone else does something stupid - which is obviously not going to happen
    return reward_function(game_state)


def _delta_function(delta, v):
    """
    Denotes the component of the of the reward vector delta associated
    with the current player p at node v
    """
    # This may need to change in a game that is for more than two players.
    # It should return a value that takes into account how well each
    # player is doing - so teammates should be maximized while enemies
    # are minimized or whatever.
    # But for two player games, you can simply return delta.
    return delta


def _expand(v):
    got_one, action_set_to_try = _try_to_get_untried_action_set(v)
    if got_one:
        # This function would need some way of approximating the units'
        # new position, given that the action set is merely attack/defend
        return v.derive_child(action_set_to_try)
    else:
        return False, None


def _try_to_get_untried_action_set(v):
    TRIES = 100 # let's say
    for i in range(TRIES):
        # This function randomly generates an action set from each
        # unit's odds of selecting attack vs defend
        # If the action set so generated has already been generated before
        # by this node, then it returns False, None
        # otherwise it returns True, action_set
        got_one, action_set = v.pull_from_most_likekly_action_sets()
    if got_one:
        return True, action_set
    else:
        v.is_fully_expanded = True
        return False, None


def _tree_policy(v):
    # This value of Cp works for rewards in the range of [0, 1]
    Cp = 1 / math.sqrt(2)
    while v.is_non_terminal():
        if not v.is_fully_expanded:
            worked, new_node = _expand(v)
            if worked:
                return new_node
            else:
                v = _best_child(v, Cp)
        else:
            v = _best_child(v, Cp)
    return v


def _within_computational_budget(start):
    """
    Returns True if time still hasn't run out for the computer's turn.
    """
    elapsed_time = process_time() - start
    return elapsed_time < 1.5



