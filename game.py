import tkinter as tk
from awale import Awale
from gui import GUI


class Game:
    AI_DELAY_MS = 600

    def __init__(self, player1, player2):
        self._awale = player1.get_awale()
        if player2.get_awale() is not self._awale:
            raise ValueError("Both players must share the same Awale instance.")

        self._players = [player1, player2]
        self._root = tk.Tk()
        self._view = GUI(self._root, self._awale)
        self._view.set_click_callback(self._on_human_click)
        self._waiting_for_human = False

    def start(self):
        self._root.after(200, self._next_turn)
        self._root.mainloop()

    def _next_turn(self):
        if self._awale.is_finished():
            self._end_game()
            return

        player_idx = self._awale.get_current_player()
        player = self._players[player_idx]
        moves = self._awale.valid_moves()

        self._view.set_message(f"Turn of {player.get_name()} — {len(moves)} possible move(s)")
        self._view.set_valid_holes(moves)
        self._view.update_view()

        from player import HumanPlayer
        if isinstance(player, HumanPlayer):
            self._waiting_for_human = True
        else:
            self._root.after(self.AI_DELAY_MS, lambda: self._play_ai(player, moves))

    def _play_ai(self, player, moves):
        move = player.choose_move(moves)
        if move is not None:
            self._awale.play(move)
            self._view.update_view()
        self._root.after(100, self._next_turn)

    def _on_human_click(self, hole):
        if not self._waiting_for_human:
            return

        player_idx = self._awale.get_current_player()
        player = self._players[player_idx]
        moves = self._awale.valid_moves()

        move = player.choose_move(moves) if hasattr(player, 'set_move') else None

        success = self._awale.play(hole)
        if success:
            self._waiting_for_human = False
            self._view.set_valid_holes([])
            self._view.update_view()
            self._root.after(150, self._next_turn)

    def _end_game(self):
        winner = self._awale.winner()
        scores = self._awale.final_scores()

        if winner == -1:
            msg = f"Draw ! ({scores[0]} - {scores[1]})"
        else:
            name = self._players[winner].get_name()
            msg = f"{name} wins ! ({scores[0]} - {scores[1]})"

        self._view.set_message(msg)
        self._view.set_valid_holes([])
        self._root.after(800, lambda: self._view.show_end(winner, scores))