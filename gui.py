import tkinter as tk
from tkinter import font as tkfont
from awale import Awale


COLORS = {
    "background":     "#2C1810",
    "board":          "#8B4513",
    "board_edge":     "#5C2E0A",
    "normal_hole":    "#A0522D",
    "hover_hole":     "#CD853F",
    "valid_hole":     "#DAA520",
    "invalid_hole":   "#6B3520",
    "selected_hole":  "#FFD700",
    "seed":           "#228B22",
    "seed_outline":   "#145214",
    "main_text":      "#F5DEB3",
    "score_text":     "#FFD700",
    "hole_text":      "#FAEBD7",
    "player1":        "#4169E1",
    "player2":        "#DC143C",
    "score_bg":       "#3D1F0D",
    "separator":      "#5C2E0A",
    "turn_highlight": "#FFD700",
}

SEED_RADIUS = 7
MAX_SEEDS_DISPLAYED = 20


class GUI:
    WIDTH = 780
    HEIGHT = 520
    MARGIN = 40
    HOLE_RADIUS = 52

    def __init__(self, root: tk.Tk, awale: Awale):
        self._awale = awale
        self._root = root
        self._click_callback = None
        self._valid_holes = []
        self._hovered_hole = None

        self._build_ui()
        self._draw_board()
        self.update_view()

    def _build_ui(self):
        self._root.title("Awalé")
        self._root.configure(bg=COLORS["background"])
        self._root.resizable(False, False)

        self._title_font = tkfont.Font(family="Georgia", size=18, weight="bold")
        self._score_font = tkfont.Font(family="Georgia", size=14, weight="bold")
        self._hole_font  = tkfont.Font(family="Georgia", size=12)
        self._info_font  = tkfont.Font(family="Georgia", size=11)
        self._small_font = tkfont.Font(family="Georgia", size=9)

        tk.Label(
            self._root, text="⬡  A W A L É  ⬡",
            font=self._title_font,
            bg=COLORS["background"], fg=COLORS["main_text"]
        ).pack(pady=(12, 4))

        self._canvas = tk.Canvas(
            self._root,
            width=self.WIDTH, height=self.HEIGHT,
            bg=COLORS["background"], highlightthickness=0
        )
        self._canvas.pack(padx=20, pady=4)
        self._canvas.bind("<Motion>",        self._on_hover)
        self._canvas.bind("<Leave>",         self._on_leave)
        self._canvas.bind("<Button-1>",      self._on_click)

        self._info_var = tk.StringVar(value="")
        self._info_label = tk.Label(
            self._root,
            textvariable=self._info_var,
            font=self._info_font,
            bg=COLORS["background"], fg=COLORS["main_text"],
            pady=6
        )
        self._info_label.pack()

    def _hole_positions(self):
        positions = {}
        margin_x = 110
        spacing = (self.WIDTH - 2 * margin_x) / 5
        y_top = self.HEIGHT // 2 - 90
        y_bottom = self.HEIGHT // 2 + 90

        for i in range(6):
            cx = margin_x + i * spacing
            positions[i] = (cx, y_bottom)
            positions[11 - i] = (cx, y_top)

        return positions

    def _draw_board(self):
        c = self._canvas
        w, h = self.WIDTH, self.HEIGHT
        r = self.HOLE_RADIUS
        positions = self._hole_positions()

        margin = 60
        c.create_rectangle(
            margin, 60, w - margin, h - 60,
            fill=COLORS["board"], outline=COLORS["board_edge"], width=3
        )

        c.create_line(
            margin + 10, h // 2, w - margin - 10, h // 2,
            fill=COLORS["separator"], width=2, dash=(8, 4)
        )

        self._draw_bank(c, 12, h // 2 - 70, h // 2 + 70, 2)
        self._draw_bank(c, w - 12, h // 2 - 70, h // 2 + 70, 1)

        c.create_text(
            w // 2, 28,
            text="Player 2", font=self._score_font,
            fill=COLORS["player2"]
        )
        c.create_text(
            w // 2, h - 28,
            text="Player 1", font=self._score_font,
            fill=COLORS["player1"]
        )

        for idx, (cx, cy) in positions.items():
            c.create_text(
                cx, cy + r + 14,
                text=str(idx),
                font=self._small_font,
                fill=COLORS["main_text"],
                tags=f"num_{idx}"
            )

    def _draw_bank(self, c, center_x, top_y, bottom_y, player):
        color = COLORS[f"player{player}"]
        width = 38
        c.create_rectangle(
            center_x - width // 2, top_y,
            center_x + width // 2, bottom_y,
            fill=COLORS["score_bg"],
            outline=color, width=2,
            tags=f"bank_{player}"
        )

    def update_view(self):
        self._canvas.delete("hole", "seed", "bank_score", "turn_indicator")
        board = self._awale.get_board()
        captures = self._awale.get_captures()
        positions = self._hole_positions()

        player_idx = self._awale.get_current_player()
        ind_y = 28 if player_idx == 1 else self.HEIGHT - 28
        self._canvas.create_oval(
            22, ind_y - 6, 34, ind_y + 6,
            fill=COLORS["turn_highlight"],
            outline="", tags="turn_indicator"
        )

        for idx, (cx, cy) in positions.items():
            self._draw_hole(idx, cx, cy, board[idx])

        self._canvas.create_text(
            12, self.HEIGHT // 2,
            text=str(captures[1]),
            font=self._score_font,
            fill=COLORS["score_text"],
            tags="bank_score"
        )
        self._canvas.create_text(
            self.WIDTH - 12, self.HEIGHT // 2,
            text=str(captures[0]),
            font=self._score_font,
            fill=COLORS["score_text"],
            tags="bank_score"
        )

    def _draw_hole(self, idx, cx, cy, nb_seeds):
        c = self._canvas
        r = self.HOLE_RADIUS

        if idx in self._valid_holes:
            color = COLORS["valid_hole"] if idx != self._hovered_hole \
                else COLORS["hover_hole"]
            outline_w = 3
        elif idx == self._hovered_hole:
            color = COLORS["invalid_hole"]
            outline_w = 1
        else:
            color = COLORS["normal_hole"]
            outline_w = 1

        c.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=color,
            outline=COLORS["board_edge"], width=outline_w,
            tags="hole"
        )

        if nb_seeds <= MAX_SEEDS_DISPLAYED:
            self._draw_seeds(cx, cy, nb_seeds)
        else:
            c.create_text(
                cx, cy,
                text=str(nb_seeds),
                font=self._score_font,
                fill=COLORS["hole_text"],
                tags="seed"
            )

        c.create_text(
            cx, cy + r - 14,
            text=str(nb_seeds),
            font=self._small_font,
            fill=COLORS["hole_text"],
            tags="hole"
        )

    def _draw_seeds(self, cx, cy, nb):
        c = self._canvas
        r = SEED_RADIUS
        import math
        positions = []
        if nb == 0:
            return
        cols = min(nb, 4)
        rows = math.ceil(nb / cols)
        spacing_x = 18
        spacing_y = 16
        start_x = cx - (cols - 1) * spacing_x / 2
        start_y = cy - (rows - 1) * spacing_y / 2

        for i in range(nb):
            col = i % cols
            row = i // cols
            gx = start_x + col * spacing_x
            gy = start_y + row * spacing_y
            positions.append((gx, gy))

        for gx, gy in positions:
            c.create_oval(
                gx - r, gy - r, gx + r, gy + r,
                fill=COLORS["seed"],
                outline=COLORS["seed_outline"], width=1,
                tags="seed"
            )

    def _hole_under_cursor(self, x, y):
        positions = self._hole_positions()
        r = self.HOLE_RADIUS
        for idx, (cx, cy) in positions.items():
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                return idx
        return None

    def _on_hover(self, event):
        hole = self._hole_under_cursor(event.x, event.y)
        if hole != self._hovered_hole:
            self._hovered_hole = hole
            self.update_view()
            if hole in self._valid_holes:
                self._canvas.configure(cursor="hand2")
            else:
                self._canvas.configure(cursor="")

    def _on_leave(self, event):
        self._hovered_hole = None
        self._canvas.configure(cursor="")
        self.update_view()

    def _on_click(self, event):
        hole = self._hole_under_cursor(event.x, event.y)
        if hole is not None and hole in self._valid_holes:
            if self._click_callback:
                self._click_callback(hole)

    def set_click_callback(self, callback):
        self._click_callback = callback

    def set_valid_holes(self, holes: list):
        self._valid_holes = holes
        self.update_view()

    def set_message(self, message: str):
        self._info_var.set(message)

    def show_end(self, winner, scores):
        self._canvas.delete("all")
        c = self._canvas
        w, h = self.WIDTH, self.HEIGHT

        c.create_rectangle(0, 0, w, h, fill=COLORS["score_bg"])

        if winner == -1:
            title = "DRAW !"
            title_color = COLORS["score_text"]
        else:
            display_winner = winner + 1
            title = f"PLAYER {display_winner} WINS !"
            title_color = COLORS[f"player{display_winner}"]

        c.create_text(
            w // 2, h // 2 - 60,
            text=title,
            font=tkfont.Font(family="Georgia", size=28, weight="bold"),
            fill=title_color
        )
        c.create_text(
            w // 2, h // 2 + 10,
            text=f"Score Player 1 : {scores[0]}   |   Score Player 2 : {scores[1]}",
            font=self._score_font,
            fill=COLORS["main_text"]
        )

        tk.Button(
            self._root, text="New game",
            font=self._info_font,
            bg=COLORS["valid_hole"], fg=COLORS["background"],
            command=self._root.destroy
        ).pack(pady=10)