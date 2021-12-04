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
        self._d = [(0, 1), (0, -1), (1, 0), (-1, 0)]

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

# pulire il codice!!!

    def control(self, x: int, y: int, c: str) -> bool:
        if 0 <= y <= self._cols and 0 <= x <= self._cols:
            if self._board[y * self._cols + x] == c:
                return True

#cerare funzione di ricerca pos una cella cerca intorno, creare funzione di riempimento, 

    def search_element_around(self, x, y):
        #data una coordinata inziale, restituisce una lista dei valori intorno alla coordinata data
        if 0 <= y <= self._rows and 0 <= x <= self._cols:
            element_around = []
            for i in self._d:
                x_n, y_n = i
                if 0 <= (y + y_n) <= self._rows-1 and 0 <= (x+x_n) <= self._cols-1:
                    element_around.append(self._board[(y + y_n) * self._cols + (x+x_n)])
                     

            return element_around
        else:
            return False


    def search_coord_around(self, x, y, c):
        #data una coordinata e un valore, restituisce una lista di coordinate
        #del valori dato, intorno al punto di partenza 
        if 0 <= y <= self._rows and 0 <= x <= self._cols:
            coord_element = []
            for i in self._d:
                x_n, y_n = i
                if 0 <= (y + y_n) <= self._rows-1 and 0 <= (x+x_n) <= self._cols-1:
                    if self._board[(y + y_n) * self._cols + (x+x_n)] == c:
                        coord_element.append(((x+x_n), (y+y_n))) 
            print(coord_element)
            return coord_element  

    def insert_around(self, x, y, c):
        #inserisce un valore in una coordinata data
        if 0 <= y <= self._rows and 0 <= x <= self._cols:
            self._board[y * self._cols + x] = c


    def auto(self, x: int, y: int):
        #automatismi

        if self.control(x, y, "+"):
            #Autocompletamento, al click su un incrocio (+)
            element_around = self.search_element_around(x,y)
            number_element = element_around.count("|")
            if number_element == 2:
                #ci sono già due linee → tutte ×
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "x")

            #manca solo una casella → linea o ×
            if element_around.count(" ") == 1 and element_around.count("x") == 3:
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "|")

            elif element_around.count(" ") == 1 and element_around.count("|") == 3:
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "x")

        
        elif 48 <= ord(self._board[y * self._cols + x]) <= 57:
            #Autocompletamento, al click su un vincolo numerico
            number = self._board[y * self._cols + x]
            element_around = self.search_element_around(x,y)
            number_element = element_around.count("|")

            if number_element == int(number):
                #ci sono già le linee giuste → tutte ×
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "x")

            elif number_element <= int(number):
                #mancano n linee e ci sono n caselle libere → tutte linee
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "|")


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
    def control_plus(self):
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]

                if val == "+":
                    number_element = 0
                    element = self.search_element_around(x, y)
                    number_element = element.count("|")
                    if not(number_element == 2 or number_element == 0):  
                        return False
        return True
                
                

    def finished(self) -> bool:
        # funzione di verfica vincita del gicoco
        count_true = 0
        # controllo che ad ogni numero ci sia il numero giusto di linee
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]
                if "0" <= val < "4":
                    numbers_line = 0
                    numbers_element= self.search_element_around(x,y)
                    numbers_line = numbers_element.count("|") 

                    if numbers_line == int(val):
                        count_true += 1

                # controllo ai segni + devono esserci 2 o 0 linee

            print(self.control_plus())
        # controllo condizioni di vittoria
        if self.control_loop():
            if (count_true == self._tot_num and self.control_plus()):
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
        
        if "LeftButton" in keys and self._mouse_down == 0:
            self._mouse_down = time()
        elif "LeftButton" not in keys and self._mouse_down > 0:
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            self._game.auto(x, (self._game._rows - y) - 1)
            if time() - self._mouse_down > LONG_PRESS:
                self._game.flag_at(x, (self._game._rows - y) - 1)
            else:
                self._game.play_at(x, (self._game._rows - y) - 1)
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