import tkinter as tk
from tkinter import font as tkfont
import math
from awale import Awale


class GUI:
    WIDTH = 780
    HEIGHT = 520
    MARGIN = 40
    HOLE_RADIUS = 52
    SEED_RADIUS = 7
    MAX_SEEDS_DISPLAYED = 20
    
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

    def __init__(self, root, awale):
        self.awale = awale
        self.root = root
        self.click_callback = None
        self.valid_holes = []
        self.hovered_hole = None

        self.build_ui()
        self.draw_board()
        self.update_view()

    def build_ui(self):
        self.root.title("Awalé")
        self.root.configure(bg=self.COLORS["background"])
        self.root.resizable(False, False)

        self.title_font = tkfont.Font(family="Georgia", size=18, weight="bold")
        self.score_font = tkfont.Font(family="Georgia", size=14, weight="bold")
        self.hole_font  = tkfont.Font(family="Georgia", size=12)
        self.info_font  = tkfont.Font(family="Georgia", size=11)
        self.small_font = tkfont.Font(family="Georgia", size=9)

        tk.Label(
            self.root, text="⬡  A W A L É  ⬡",
            font=self.title_font,
            bg=self.COLORS["background"], fg=self.COLORS["main_text"]
        ).pack(pady=(12, 4))

        self.canvas = tk.Canvas(
            self.root,
            width=self.WIDTH, height=self.HEIGHT,
            bg=self.COLORS["background"], highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=4)
        self.canvas.bind("<Motion>",        self.on_hover)
        self.canvas.bind("<Leave>",         self.on_leave)
        self.canvas.bind("<Button-1>",      self.on_click)

        self.info_var = tk.StringVar(value="")
        self.info_label = tk.Label(
            self.root,
            textvariable=self.info_var,
            font=self.info_font,
            bg=self.COLORS["background"], fg=self.COLORS["main_text"],
            pady=6
        )
        self.info_label.pack()

    def hole_positions(self):
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

    def draw_board(self):
        c = self.canvas
        w, h = self.WIDTH, self.HEIGHT
        r = self.HOLE_RADIUS
        positions = self.hole_positions()

        margin = 60
        c.create_rectangle(
            margin, 60, w - margin, h - 60,
            fill=self.COLORS["board"], outline=self.COLORS["board_edge"], width=3
        )

        c.create_line(
            margin + 10, h // 2, w - margin - 10, h // 2,
            fill=self.COLORS["separator"], width=2, dash=(8, 4)
        )

        self.draw_bank(c, 12, h // 2 - 70, h // 2 + 70, 2)
        self.draw_bank(c, w - 12, h // 2 - 70, h // 2 + 70, 1)

        c.create_text(
            w // 2, 28,
            text="Player 2", font=self.score_font,
            fill=self.COLORS["player2"]
        )
        c.create_text(
            w // 2, h - 28,
            text="Player 1", font=self.score_font,
            fill=self.COLORS["player1"]
        )

        for idx, (cx, cy) in positions.items():
            c.create_text(
                cx, cy + r + 14,
                text=str(idx),
                font=self.small_font,
                fill=self.COLORS["main_text"],
                tags=f"num_{idx}"
            )

    def draw_bank(self, c, center_x, top_y, bottom_y, player):
        color = self.COLORS[f"player{player}"]
        width = 38
        c.create_rectangle(
            center_x - width // 2, top_y,
            center_x + width // 2, bottom_y,
            fill=self.COLORS["score_bg"],
            outline=color, width=2,
            tags=f"bank_{player}"
        )

    def update_view(self):
        self.canvas.delete("hole", "seed", "bank_score", "turn_indicator")
        board = self.awale.get_board()
        captures = self.awale.get_captures()
        positions = self.hole_positions()

        player_idx = self.awale.get_current_player()
        ind_y = 28 if player_idx == 1 else self.HEIGHT - 28
        self.canvas.create_oval(
            22, ind_y - 6, 34, ind_y + 6,
            fill=self.COLORS["turn_highlight"],
            outline="", tags="turn_indicator"
        )

        for idx, (cx, cy) in positions.items():
            self.draw_hole(idx, cx, cy, board[idx])

        self.canvas.create_text(
            12, self.HEIGHT // 2,
            text=str(captures[1]),
            font=self.score_font,
            fill=self.COLORS["score_text"],
            tags="bank_score"
        )
        self.canvas.create_text(
            self.WIDTH - 12, self.HEIGHT // 2,
            text=str(captures[0]),
            font=self.score_font,
            fill=self.COLORS["score_text"],
            tags="bank_score"
        )

    def draw_hole(self, idx, cx, cy, nb_seeds):
        c = self.canvas
        r = self.HOLE_RADIUS

        if idx in self.valid_holes:
            color = self.COLORS["valid_hole"] if idx != self.hovered_hole \
                else self.COLORS["hover_hole"]
            outline_w = 3
        elif idx == self.hovered_hole:
            color = self.COLORS["invalid_hole"]
            outline_w = 1
        else:
            color = self.COLORS["normal_hole"]
            outline_w = 1

        c.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=color,
            outline=self.COLORS["board_edge"], width=outline_w,
            tags="hole"
        )

        if nb_seeds <= self.MAX_SEEDS_DISPLAYED:
            self.draw_seeds(cx, cy, nb_seeds)
        else:
            c.create_text(
                cx, cy,
                text=str(nb_seeds),
                font=self.score_font,
                fill=self.COLORS["hole_text"],
                tags="seed"
            )

        c.create_text(
            cx, cy + r - 14,
            text=str(nb_seeds),
            font=self.small_font,
            fill=self.COLORS["hole_text"],
            tags="hole"
        )

    def draw_seeds(self, cx, cy, nb):
        c = self.canvas
        r = self.SEED_RADIUS
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
                fill=self.COLORS["seed"],
                outline=self.COLORS["seed_outline"], width=1,
                tags="seed"
            )

    def hole_under_cursor(self, x, y):
        positions = self.hole_positions()
        r = self.HOLE_RADIUS
        for idx, (cx, cy) in positions.items():
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                return idx
        return None

    def on_hover(self, event):
        hole = self.hole_under_cursor(event.x, event.y)
        if hole != self.hovered_hole:
            self.hovered_hole = hole
            self.update_view()
            if hole in self.valid_holes:
                self.canvas.configure(cursor="hand2")
            else:
                self.canvas.configure(cursor="")

    def on_leave(self, event):
        self.hovered_hole = None
        self.canvas.configure(cursor="")
        self.update_view()

    def on_click(self, event):
        hole = self.hole_under_cursor(event.x, event.y)
        if hole is not None and hole in self.valid_holes:
            if self.click_callback:
                self.click_callback(hole)

    def set_click_callback(self, callback):
        self.click_callback = callback

    def set_valid_holes(self, holes):
        self.valid_holes = holes
        self.update_view()

    def set_message(self, message):
        self.info_var.set(message)

    def show_end(self, winner, scores):
        self.canvas.delete("all")
        c = self.canvas
        w, h = self.WIDTH, self.HEIGHT

        c.create_rectangle(0, 0, w, h, fill=self.COLORS["score_bg"])

        if winner == -1:
            title = "DRAW !"
            title_color = self.COLORS["score_text"]
        else:
            display_winner = winner + 1
            title = f"PLAYER {display_winner} WINS !"
            title_color = self.COLORS[f"player{display_winner}"]

        c.create_text(
            w // 2, h // 2 - 60,
            text=title,
            font=tkfont.Font(family="Georgia", size=28, weight="bold"),
            fill=title_color
        )
        c.create_text(
            w // 2, h // 2 + 10,
            text=f"Score Player 1 : {scores[0]}   |   Score Player 2 : {scores[1]}",
            font=self.score_font,
            fill=self.COLORS["main_text"]
        )

        tk.Button(
            self.root, text="New game",
            font=self.info_font,
            bg=self.COLORS["valid_hole"], fg=self.COLORS["background"],
            command=self.root.destroy
        ).pack(pady=10)
