"""
Module for holding the Node class.
"""

class Node:
    """
    This class is essentially just a GameState, but with some
    helper functions and additional data (such as parent and children).
    """
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []
        self.total_reward = 0
        self.num_times_visited = 0

    def available_actions(self):
        """
        Returns the set of available moves that could be applied to
        this Node's state.
        """
        return self.state.possible_moves()

    def derive_child(action):
        """
        Derives a new Node from this one and the given action.
        """
        child_state = self.state.deep_copy()
        child_state.take_turn(action)
        child_node = Node(child_state)
        self.children.append(child_node)
        return child_node

    def is_non_terminal(self):
        """
        A Node is terminal if its state is at game over.
        So this returns True as long as that is not the case.
        """
        return not self.state.game_over()

    def is_not_fully_expanded(self):
        """
        Returns whether or not all possible children have been
        added to this Node.
        """
        return len(self.available_actions()) == len(self.children)
