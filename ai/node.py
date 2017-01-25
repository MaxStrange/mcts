"""
Module for holding the Node class.
"""

import copy
import os

class Node:
    """
    This class is essentially just a GameState, but with some
    helper functions and additional data (such as parent and children).
    """
    def __init__(self, state):
        self.name = None
        self.state = state
        self.parent = None
        self.children = []
        self.total_reward = 0
        self.num_times_visited = 0
        self.already_tried_actions = []

    def __str__(self):
        s = "Node: "
        for key, val in self.__dict__.items():
            s += os.linesep + "    " + key + ": " + str(val)
        return s

    def available_actions(self):
        """
        Returns the set of available moves that could be applied to
        this Node's state.
        """
        return self.state.possible_moves()

    def derive_child(self, action):
        """
        Derives a new Node from this one and the given action.
        """
        child_state = copy.deepcopy(self.state)
        child_state.take_turn(action)
        child_node = Node(child_state)
        child_node.parent = self
        child_node.name = self.name + "_" + str(child_node.move_that_derived_this_node())
        self.children.append(child_node)
        self.already_tried_actions.append(action)
        return child_node

    def move_that_derived_this_node(self):
        """
        Returns the action that created this Node's game state.
        """
        return self.state._move_that_derived_this_state

    def is_non_terminal(self):
        """
        A Node is terminal if its state is at game over.
        So this returns True as long as that is not the case.
        """
        return not self.state.game_over()

    def is_not_fully_expanded(self):
        """
        Returns True unless all possible children have been added to this
        Node's children list.
        """
        return len(self.available_actions()) != len(self.children)







