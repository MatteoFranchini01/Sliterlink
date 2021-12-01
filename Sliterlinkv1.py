import g2d
from time import time

W, H = 40, 40
LONG_PRESS = 0.5


class Slitherlink:
    def __init__(self):

        count_rows = 0
        count_num = 0
        count_num_line = 0
        lista = []
        with open("game_nowin_5x5.txt") as b:
            for line in b:
                board = line.strip("\n")  # Legge la matrice togliendo \n alla fine della riga
                lista += board
                count_rows += 1
        for x in lista:
            if 48 <= ord(x) <= 57:
                count_num += 1
            # conta le linee
            elif x == "|" or x == "x":
                count_num_line += 1

        self._cols = len(board)
        self._rows = count_rows
        self._board = lista
        self._tot_num = count_num
        self._num_line_loop = 0
        self._num_line = count_num_line
        self._start_line = (0, 0)
        self._coord = (0, 0)
        self._c = True

    def cols(self) -> int:
        return self._cols

    def rows(self) -> int:
        return self._rows

    def play_at(self, x: int, y: int):
        if self.control(x, y, " "):
            self._board[y * self._cols + x] = "|"
        elif self.control(x, y, "|") or self.control(x, y, "x"):
            self._board[y * self._cols + x] = " "
        else:
            return

    def flag_at(self, x: int, y: int):
        print("flag", x, y)
        if self.control(x, y, " ") or self.control(x, y, "|"):
            self._board[y * self._cols + x] = "x"
        else:
            return

    def value_at(self, x: int, y: int) -> str:
        if self.control(x, y, "|"):
            if self.control(x-1, y, "+") and self.control(x+1, y, "+"):
                return "-"
            if self.control(x, y-1, "+") and self.control(x, y+1, "+"):
                return "|"

        return self._board[y * self._cols + x]

    def message(self):
        if self.finished():
            return "won"

    def control(self, x: int, y: int, c: str) -> bool:
        if self._board[y * self._cols + x] == c:
            return True

    def auto(self, x: int, y: int):
        count = 0
        if self.control(x, y, "+"):
            if self.control(x, y+1, "|") and y < self._cols:
                count += 1
            if self.control(x, y-1, "|") and y > 0:
                count += 1
            if self.control(x+1, y, "|") and x < self._rows:
                count += 1
            if self.control(x-1, y, "|") and x > 0:
                count += 1

            if count == 2: # se ci sono due linee le altre sono x
                if self.control(x, y+1, " ") and y < self._cols:
                    self._board[y + 1 * self._cols + x] = "x"
                if self.control(x, y-1, " ") and y > 0:
                    self._board[y - 1 * self._cols + x] = "x"
                if self.control(x+1, y, " ") and x < self._rows:
                    self._board[y * self._cols + x + 1] = "x"
                if self.control(x-1, y, " ") and x > 0:
                    self._board[y * self._cols + x - 1] = "x"

        if 48 <= ord(self._board[y * self._cols + x]) <= 57:

            if self.control(x, y+1, "|") and y < self._cols:
                count += 1
            if self.control(x, y-1, "|") and y > 0:
                count += 1
            if self.control(x+1, y, "|") and x < self._rows:
                count += 1
            if self.control(x-1, y, "|") and x > 0:
                count += 1

            if count == int(self._board[y * self._cols + x]): #se ci sono tutte le linee giuste le altre sono x
                if self.control(x, y+1, " ") and y < self._cols:
                    self._board[y + 1 * self._cols + x] = "x"
                if self.control(x, y-1, " ") and y > 0:
                    self._board[y - 1 * self._cols + x] = "x"
                if self.control(x+1, y, " ") and x < self._rows:
                    self._board[y * self._cols + x + 1] = "x"
                if self.control(x-1, y, " ") and x > 0:
                    self._board[y * self._cols + x - 1] = "x"


    def control_loop(self):
        # funzione controllo single loop
        self._num_line = self._board.count("|") + self._board.count("+")  # conto quanti | e + ci sono nella lista

        self._start_line = (0, 0)

        # ricerca della prima linea da cui iniziare il single loop
        if self._start_line == (0, 0):
            for x in range(self._cols):
                for y in range(self._rows):
                    val = self._board[y * self._cols + x]
                    if val == "|":
                        self._start_line = (x, y)

        y, x = self._start_line
        old_x = 0
        old_y = 0
        i = 0
        self._num_line_loop = 0
        start_coord = (x, y)
        control = "+"
        # ricerca del single loop
        for i in range(self._num_line):
            if (y < self._rows - 1) and (self._board[(y + 1) * self._cols + (x)] == control) and (
                    x != old_x or (y + 1) != old_y):
                old_x, old_y = x, y  # memorizzo la vecchia posizione
                self._num_line_loop += 1  # conto  quanti "|" / + ci sono
                x, y = (x, y + 1)

            elif (y > 0) and (self._board[(y - 1) * self._cols + (x)] == control) and (x != old_x or (y - 1) != old_y):
                old_x, old_y = x, y
                self._num_line_loop += 1
                x, y = (x, y - 1)

            elif (x < self._cols - 1) and (self._board[(y) * self._cols + (x + 1)] == control) and (
                    (x + 1) != old_x or y != old_y):
                old_x, old_y = x, y
                self._num_line_loop += 1
                x, y = (x + 1, y)

            elif (x > 0) and (self._board[(y) * self._cols + (x - 1)] == control) and ((x - 1) != old_x or y != old_y):
                old_x, old_y = x, y
                self._num_line_loop += 1
                x, y = (x - 1, y)

            # cambio il valore di ricerca
            if control == "|":
                control = "+"

            elif control == "+":
                control = "|"

            # se le coordinate sono uguali a quelle iniziali (sono arrivato al punto di paretnza, ho un percorso chiuso)
            if (x, y) == start_coord:
                return True

        # se i + e le "|" che ho contato sono uguali a quelle in totale
        if self._num_line == self._num_line_loop:
            return True
        else:
            return False

    def finished(self) -> bool:
        # funzione di verfica vincita del gicoco
        risult_plus = False
        cont = 0
        count_true = 0
        # controllo che dificano ad ogni numero ci sia il numero giusto di linee
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]
                if "0" <= val < "4":
                    cont = 0
                    if self.control(x, y+1,"|"):
                        cont += 1
                    if self.control(x, y-1, "|"):
                        cont += 1
                    if self.control(x+1, y, "|"):
                        cont += 1
                    if self.control(x-1, y, "|"):
                        cont += 1

                    if cont == int(val):
                        count_true += 1

                # controllo ai segni + devono esserci 2 o 0 linee
                elif val == "+":
                    cont = 0

                    if y < 0 and self.control(x, y+1, "|"):
                        cont += 1
                    if y > self._rows and self.control(x, y-1, "|"):
                        cont += 1
                    if x > self._cols and self.control(x+1, y, "|"):
                        cont += 1
                    if x < 0 and self.control(x-1, y, "|"):
                        cont += 1

                    if cont == 2 or cont == 0:
                        risult_plus = True
                    else:
                        risult_plus = False

        # controllo condizioni di vittoria
        if self.control_loop():
            if (count_true == self._tot_num and risult_plus):
                return True
            else:
                return False



class BoardGameGui:
    def __init__(self, g: Slitherlink):
        self._game = g
        self._mouse_down = 0
        self._prev_keys = set()
        self.update_buttons()

    def tick(self):
        keys = set(g2d.current_keys())
        rows = 11
        if "LeftButton" in keys and self._mouse_down == 0:
            self._mouse_down = time()
        elif "LeftButton" not in keys and self._mouse_down > 0:
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            self._game.auto(x, y)
            if time() - self._mouse_down > LONG_PRESS:
                self._game.flag_at(x, (rows - y) - 1)
            else:
                self._game.play_at(x, (rows - y) - 1)
            self.update_buttons()
            self._mouse_down = 0

        if "Escape" in (self._prev_keys - keys):  # "Escape" key released
            g2d.close_canvas()
        self._prev_keys = keys
        self._game.control_loop()  # CANCELLARE

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
                value = str(self._game.value_at(x, (rows - y) - 1))
                center = x * W + W // 2, y * H + H // 2
                g2d.draw_text_centered(value, center, H // 2)
        if self._game.finished():
            g2d.alert(self._game.message())
            # g2d.close_canvas()


def gui_play(game: Slitherlink):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)


s = Slitherlink()
gui_play(s)
