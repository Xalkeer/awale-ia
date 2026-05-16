import tkinter as tk
from awale import Awale
from gui import GUI


class Game:
    AI_DELAY_MS = 600

    def __init__(self, player1, player2, awale=None):
        """Initialise la partie.

        player1/player2 peuvent être :
          - des objets exposant get_awale(), get_name(), choose_move(valid_moves)
          - ou des IA comme MCTS qui exposent choose_move(awale)

        On accepte aussi de passer explicitement une instance `awale`.
        """
        # déterminer l'instance Awale à utiliser
        if awale is not None:
            self.awale = awale
        else:
            # essayer d'obtenir via get_awale() si disponible
            a = None
            for p in (player1, player2):
                try:
                    a = p.get_awale()
                    break
                except Exception:
                    # p n'expose pas get_awale()
                    a = None
            # si toujours None, créer une nouvelle instance
            self.awale = a if a is not None else Awale()

        # vérifier que, si un joueur fournit get_awale, il correspond à self.awale
        for p in (player1, player2):
            try:
                pa = p.get_awale()
            except Exception:
                pa = None
            if pa is not None and pa is not self.awale:
                raise ValueError("Both players must share the same Awale instance.")

        self.players = [player1, player2]
        self.root = tk.Tk()
        self.view = GUI(self.root, self.awale)
        self.view.set_click_callback(self.on_human_click)
        self.waiting_for_human = False

    def start(self):
        self.root.after(200, self.next_turn)
        self.root.mainloop()

    def next_turn(self):
        if self.awale.is_finished():
            self.end_game()
            return

        player_idx = self.awale.get_current_player()
        player = self.players[player_idx]
        moves = self.awale.valid_moves()

        self.view.set_message(f"Turn of {player.get_name()} — {len(moves)} possible move(s)")
        self.view.set_valid_holes(moves)
        self.view.update_view()

        from player import HumanPlayer
        if isinstance(player, HumanPlayer):
            self.waiting_for_human = True
        else:
            self.root.after(self.AI_DELAY_MS, lambda: self.play_ai(player, moves))

    def play_ai(self, player, moves):
        # Certains bots (MinMax, StupidBot) attendent choose_move(valid_moves)
        # D'autres (MCTS) attendent choose_move(awale). On essaye les deux.
        try:
            move = player.choose_move(moves)
        except TypeError:
            # signature différente : essayer en passant l'état complet
            try:
                move = player.choose_move(self.awale)
            except Exception:
                # Ne pas interrompre l'UI ; retourner None
                move = None
        if move is not None:
            self.awale.play(move)
            self.view.update_view()
        self.root.after(100, self.next_turn)

    def on_human_click(self, hole):
        if not self.waiting_for_human:
            return

        player_idx = self.awale.get_current_player()
        player = self.players[player_idx]
        moves = self.awale.valid_moves()

        move = player.choose_move(moves) if hasattr(player, 'set_move') else None

        success = self.awale.play(hole)
        if success:
            self.waiting_for_human = False
            self.view.set_valid_holes([])
            self.view.update_view()
            self.root.after(150, self.next_turn)

    def end_game(self):
        winner = self.awale.winner()
        scores = self.awale.final_scores()

        if winner == -1:
            msg = f"Draw ! ({scores[0]} - {scores[1]})"
        else:
            name = self.players[winner].get_name()
            msg = f"{name} wins ! ({scores[0]} - {scores[1]})"

        self.view.set_message(msg)
        self.view.set_valid_holes([])
        self.root.after(800, lambda: self.view.show_end(winner, scores))
