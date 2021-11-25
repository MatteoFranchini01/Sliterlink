import g2d
from time import time

W, H = 40, 40
LONG_PRESS = 0.5

class Slitherlink:
    def __init__(self):
        lista = []
        with open("game_5x5.txt") as b:
            for line in b:
                board = line.strip("\n")  # Legge la matrice togliendo \n alla fine della riga
                lista += board
        self._board = lista
        self._rows = 11
        self._cols = 11

    def cols(self) -> int:
        return self._cols

    def rows(self) -> int:
        return self._rows

    def play_at(self, x: int, y: int):
        if self._board[y * self._cols + x] == " ":
            self._board[y * self._cols + x] = "|"
        else:
            return

    def flag_at(self, x: int, y: int):
        if self._board[y * self._cols + x] == " ":
            self._board[y * self._cols + x] = "x"
        else:
            return

    def value_at(self, x: int, y: int) -> str:
        return self._board[y * self._cols + x]

    def finished(self) -> bool:
        coord_plus = []
        coord_number = []
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]
                if val == "+":
                    coord_plus.append(val)
                elif val != " ":
                    coord_number.append(val)

class BoardGameGui:
    def __init__(self, g: Slitherlink):
        self._game = g
        self._mouse_down = 0
        self._prev_keys = set()
        self.update_buttons()

    def tick(self):
        keys = set(g2d.current_keys())
        if "LeftButton" in keys and self._mouse_down == 0:
            self._mouse_down = time()
        elif "LeftButton" not in keys and self._mouse_down > 0:
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._mouse_down > LONG_PRESS:
                self._game.flag_at(x, y)
            else:
                self._game.play_at(x, y)
            self.update_buttons()
            self._mouse_down = 0

        if "Escape" in (self._prev_keys - keys):  # "Escape" key released
            g2d.close_canvas()
        self._prev_keys = keys

    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
        for y in range(rows):
            for x in range(cols):
                value = str(self._game.value_at(x, y))
                center = x * W + W//2, y * H + H//2
                g2d.draw_text_centered(value, center, H//2)
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()

def gui_play(game: Slitherlink):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)

s = Slitherlink()
gui_play(s)
