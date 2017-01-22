"""
This is the pseudo code for the UCT (Upper Confidence Bounds for Trees)
algorithm.
"""

def uct_search(game_state):
    root = Node(game_state)

    while within_computational_budget():
        v = tree_policy(root)
        delta = default_policy(v.state)
        back_up(v, delta)
 
    # This will usually, but not always, return the action that leads
    # to the child with the highest reward. It COULD (since Cp is set
    # to zero for this call) return the node that is most visited instead.
    # This is often the node that is the best, but not always. So,
    # one possible improvement is to check if the most visited root
    # action is not also the one with the highest reward, and if it isn't,
    # keep searching.
    return best_child(v, 0).incoming_action

def tree_policy(v):
    # This value of Cp works for rewards in the range of [0, 1]
    Cp = 1 / math.sqrt(2)
    while non_terminal(v):
        if not_fully_expanded(v):
            return expand(v)
        else:
            v = best_child(v, Cp)
    return v

def expand(v):
    action_to_try = choose_untried_action_from(A(v.state))
    v_prime = v.derive_child(v.state.apply_action(action_to_try))
    return v_prime

def best_child(v, c):
    def valfunc(v_prime, v):
        left = v_prime.total_reward / v_prime.num_times_visited
        right = c * math.sqrt((2 * math.ln(v.num_times_visited))\
                / v_prime.num_times_visited)
        return left + right
    values = [valfunc(v_prime, v) for v_prime in v.children()]
    return max(values)

def default_policy(game_state):
    while non_terminal(game_state):
        # This function would probably be replaced with the policy network
        action = uniform_random_choice(game_state.all_possible_actions)
        game_state = game_state.apply_action(action)
    return reward(game_state)

def back_up(v, delta):
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
        v.total_reward += delta_function(v, player)
        v = v.parent()

def delta_function(v, player):
    """
    Denotes the component of the of the reward vector delta associated
    with the current player p and node v
    """
    pass







