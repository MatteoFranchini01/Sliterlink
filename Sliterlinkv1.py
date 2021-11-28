from os import truncate
import g2d
from time import time

W, H = 40, 40
LONG_PRESS = 0.5


class Slitherlink:
    def __init__(self):
        lista = []
        with open("game_nowin_5x5.txt") as b:
            for line in b:
                board = line.strip("\n")  # Legge la matrice togliendo \n alla fine della riga
                lista += board
        self._board = lista
        self._rows = 11
        self._cols = 11
        self._num = 11
        self._num_line_loop = 0
        self._num_line = 0
        self._start_line = (0, 0)
        self._old_coord = (0, 0)
        self._c = True

    def cols(self) -> int:
        return self._cols

    def rows(self) -> int:
        return self._rows

    def play_at(self, x: int, y: int):
        if self._board[y * self._cols + x] == " ":
            self._board[y * self._cols + x] = "|"
        elif self._board[y * self._cols + x] == "|" or self._board[y * self._cols + x] == "x":
            self._board[y * self._cols + x] = " "
        else:
            return

    def flag_at(self, x: int, y: int):
        if self._board[y * self._cols + x] == " " or self._board[y * self._cols + x] == "|":
            self._board[y * self._cols + x] = "x"
        else:
            return

    def value_at(self, x: int, y: int) -> str:
        if self._board[y * self._cols + x] == "|":
            if self._board[y * self._cols + (x - 1)] == "+" and self._board[y * self._cols + (x + 1)] == "+":
                return "-"
            if self._board[(y - 1) * self._cols + (x)] == "+" and self._board[(y + 1) * self._cols + (x)] == "+":
                return "|"

        return self._board[y * self._cols + x]

    def message(self):
        if self.finished():
            return "won"
        else:
            return "sei bello come raul"


    def finished(self) -> bool:
        risult_num = False
        risult_plus = False
        cont = 0
        count_true = 0
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]
                if "0" <= val < "4":
                    cont = 0
                    if self._board[(y + 1) * self._cols + (x)] == "|":
                        cont += 1
                    if self._board[(y - 1) * self._cols + (x)] == "|":
                        cont += 1
                    if self._board[(y) * self._cols + (x + 1)] == "|":
                        cont += 1
                    if self._board[(y) * self._cols + (x - 1)] == "|":
                        cont += 1

                    if cont == int(val):
                        risult_num = True
                        count_true += 1
                    else:
                        risult_num = False

                elif val == "+":
                    cont = 0

                    if y < 0 and self._board[(y + 1) * self._cols + (x)] == "|":
                        cont += 1
                    if y > self._rows and (self._board[(y - 1) * self._cols + (x)] == "|"):
                        cont += 1
                    if x > self._cols and (self._board[(y) * self._cols + (x + 1)] == "|"):
                        cont += 1
                    if x < 0 and (self._board[(y) * self._cols + (x - 1)] == "|"):
                        cont += 1

                    if cont == 2 or cont == 0:
                        risult_plus = True
                    else:
                        risult_plus = False

        if count_true == self._num and risult_plus:
            return True
        else:
            return False



    def control_board(self, x, y, control: str) -> bool:
        # PROBELMA VARIABILE self._old_coord,  non tiene in memeoria la vecchia posizione(debug)
        for i in range(self._num_line):

            if (y < 10) and (self._board[(y + 1) * self._cols + (x)] == control) and (x, y + 1) != self._old_coord :
                self._num_line_loop +=1
                self._old_coord = (x, y + 1)

            elif (y > 0) and (self._board[(y - 1) * self._cols + (x)] == control ) and (x, y - 1) != self._old_coord:
                self._num_line_loop +=1
                self._old_coord = (x, y - 1)
        
            elif (x < self._cols) and (self._board[(y) * self._cols + (x + 1)] == control) and (x + 1, y) != self._old_coord :
                self._num_line_loop +=1
                self._old_coord = (x + 1, y)
                
            elif (x > 0) and (self._board[(y) * self._cols + (x - 1)] == control) and (x - 1, y) != self._old_coord :
                self._num_line_loop +=1
                self._old_coord = (x - 1, y)
            
            if control =="|":
                control ="+"

            elif control == "+":
                control = "|" 

            y, x = self._old_coord 

        if self._num_line_loop == self._num_line:
            #if self._start_line == self._old_coord:
            return True
        else:
            return False
        
                
       



    def control_loop(self):
        self._start_line = (0, 0)
        cont = 0
        b = False
        if not b:
            for x in range(self._cols):
                for y in range(self._rows):
                    val = self._board[y * self._cols + x]
                    if val == "|":
                        self._start_line = (x, y)
                        b = True
                        
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]
                if val == "|" or val == "x":
                   self._num_line +=1

        y, x = self._start_line
        r = self.control_board(x, y, "+")
        print(r)

        #risult = self.control_board(self._start_line, "+")
        #print(risult)
'''
            x, y = start_line
            val = self._board[y * self._cols + x]
            if val == "|":
                self.control_board(x, y, val)
            elif val == "+":
                self.control_board(x, y, val)

        v = self.control_board(start_line, "+")
        self.control_board(v, "|")
        print(start_line)
        return start_line
'''


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
        self._game.control_loop() #CANCELLARE

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