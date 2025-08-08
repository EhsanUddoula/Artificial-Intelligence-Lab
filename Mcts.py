#This is MCTS for the game of tic-tac-toe

import random
import math
import copy
from collections import defaultdict

# Constants
EMPTY, X, O = '.', 'X', 'O'

# --- Board Class ---
class Board:
    def __init__(self):
        self.board = [EMPTY] * 9
        self.turn = X

    def copy(self):
        return copy.deepcopy(self)

    def legal_moves(self):
        return [i for i in range(9) if self.board[i] == EMPTY]

    def make_move(self, idx):
        if self.board[idx] == EMPTY:
            self.board[idx] = self.turn
            self.turn = X if self.turn == O else O

    def winner(self):
        lines = [(0,1,2), (3,4,5), (6,7,8),
                 (0,3,6), (1,4,7), (2,5,8),
                 (0,4,8), (2,4,6)]
        for i,j,k in lines:
            if self.board[i] == self.board[j] == self.board[k] != EMPTY:
                return self.board[i]
        if EMPTY not in self.board:
            return 'DRAW'
        return None

    def __str__(self):
        return "\n".join([" ".join(self.board[i:i+3]) for i in range(0, 9, 3)])

# --- MCTS Node ---
class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = state.legal_moves()

    def expand(self):
        move = self.untried_moves.pop()
        next_state = self.state.copy()
        next_state.make_move(move)
        child = MCTSNode(next_state, parent=self, move=move)
        self.children.append(child)
        return child

    def best_child(self, c_param=1.41):
        choices = [(child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
                   for child in self.children]
        return self.children[choices.index(max(choices))]

    def backpropagate(self, result):
        self.visits += 1
        if result == self.state.turn:  # opponent wins
            self.wins += 0
        elif result == 'DRAW':
            self.wins += 0.5
        else:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.state.winner() is not None

# --- MCTS Function ---
def mcts(root_state, iterations=1000):
    root = MCTSNode(root_state)

    for _ in range(iterations):
        node = root
        # Selection
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        # Expansion
        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()

        # Simulation
        sim_state = node.state.copy()
        while sim_state.winner() is None:
            sim_state.make_move(random.choice(sim_state.legal_moves()))

        # Backpropagation
        node.backpropagate(sim_state.winner())

    # Choose the most visited move
    best_move = max(root.children, key=lambda n: n.visits).move
    return best_move

# --- Play a Game ---
def play_game():
    board = Board()
    while board.winner() is None:
        print(board, "\n")
        if board.turn == X:
            move = mcts(board, iterations=1000)
        else:
            move = random.choice(board.legal_moves())
        board.make_move(move)

    print(board)
    print("Winner:", board.winner())

# --- Run the Game ---
if __name__ == "__main__":
    play_game()
