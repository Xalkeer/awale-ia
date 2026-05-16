import math
import time
from random import choice


class Node:
    def __init__(self, player_id, state, parent=None):
        self.player_id = player_id
        self.state = state
        self.parent = parent
        self.children = []
        self.moves = []
        self.u = 0.0
        self.n = 0.0

    def get_state(self):
        return self.state

    def get_player_id(self):
        return self.player_id

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_moves(self):
        return self.moves

    def get_u(self):
        return self.u

    def get_n(self):
        return self.n

    def set_state(self, s):
        self.state = s

    def set_player_id(self, p):
        self.player_id = p

    def set_parent(self, p):
        self.parent = p

    def set_u(self, u):
        self.u = u

    def set_n(self, n):
        self.n = n

    def available_moves(self):
        return self.state.valid_moves()

    def is_terminal(self):
        return self.state.is_finished()

    def fully_expanded(self):
        return len(self.children) == len(self.available_moves())

    def add_child(self, child_node, move):
        self.children.append(child_node)
        self.moves.append(move)

    def update(self, result, mcts_player):
        self.n += 1.0
        if result == mcts_player:
            self.u += 1.0
        elif result == -1:
            self.u += 0.5

    def __repr__(self):
        return (f"Node(player={self.player_id}, "
                f"n={self.n:.0f}, u={self.u:.1f})")


class MCTS:
    def __init__(self, player_id, max_iterations=500, max_time=None, c=math.sqrt(2)):
        self.player_id = player_id
        self.max_iterations = max_iterations
        self.max_time = max_time
        self.c = c

    def get_player_id(self):
        return self.player_id

    def get_max_iterations(self):
        return self.max_iterations

    def get_max_time(self):
        return self.max_time

    def get_c(self):
        return self.c

    def set_max_iterations(self, n):
        self.max_iterations = n

    def set_max_time(self, t):
        self.max_time = t

    def set_c(self, c):
        self.c = c

    def choose_move(self, awale):
        root_state = awale.copy()
        root = Node(player_id=1 - root_state.get_current_player(),
                    state=root_state,
                    parent=None)

        moves = root.available_moves()
        if len(moves) == 1:
            return moves[0]

        self.run(root)
        return self.best_move(root)

    def run(self, root):
        deadline = (time.time() + self.max_time) if self.max_time else None
        iteration = 0

        while True:
            if deadline:
                if time.time() >= deadline:
                    break
            else:
                if iteration >= self.max_iterations:
                    break

            selected = self.select(root)
            leaf = self.expand(selected)
            result = self.simulate(leaf)
            self.backpropagate(leaf, result)
            iteration += 1

    def select(self, node):
        while not node.is_terminal():
            if not node.fully_expanded():
                return node
            node = self.best_child_uct(node)
        return node

    def expand(self, node):
        if node.is_terminal():
            return node

        explored_moves = node.get_moves()
        for move in node.available_moves():
            if move not in explored_moves:
                new_state = node.get_state().copy()
                new_state.play(move)
                child = Node(
                    player_id=1 - new_state.get_current_player(),
                    state=new_state,
                    parent=node
                )
                node.add_child(child, move)
                return child
        return node

    def simulate(self, node):
        sim_state = node.get_state().copy()

        while not sim_state.is_finished():
            moves = sim_state.valid_moves()
            if not moves:
                break
            sim_state.play(choice(moves))

        return sim_state.winner()

    def backpropagate(self, node, result):
        current = node
        while current is not None:
            current.update(result, self.player_id)
            current = current.get_parent()

    def best_child_uct(self, node):
        best_score = float('-inf')
        best_children = []

        for child in node.get_children():
            if child.get_n() == 0:
                return child
            exploit = child.get_u() / child.get_n()
            explore = math.sqrt(math.log(node.get_n()) / child.get_n())
            score = exploit + self.c * explore
            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)

        return choice(best_children)

    def best_move(self, root):
        if not root.get_children():
            return choice(root.available_moves())

        best_n = -1
        best_moves = []

        for child, move in zip(root.get_children(), root.get_moves()):
            if child.get_n() > best_n:
                best_n = child.get_n()
                best_moves = [move]
            elif child.get_n() == best_n:
                best_moves.append(move)

        return choice(best_moves)