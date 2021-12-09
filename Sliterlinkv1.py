import g2d
from time import time

W, H = 40, 40
LONG_PRESS = 0.2


class Slitherlink:
    def __init__(self, c):

        count_rows = 0
        count_num = 0
        count_num_line = 0
        self._game_mode1 = c
        lista = []
        with open(self._game_mode1) as b:
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
        if self.control(x, y, " ") or self.control(x, y, "|"):
            self._board[y * self._cols + x] = "x"
        else:
            return

    def value_at(self, x: int, y: int) -> str:
        if self.control(x, y, "|"):
            if self.control(x - 1, y, "+") and self.control(x + 1, y, "+"):
                return "-"
            if self.control(x, y - 1, "+") and self.control(x, y + 1, "+"):
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

    # cerare funzione di ricerca pos una cella cerca intorno, creare funzione di riempimento,

    def search_element_around(self, x, y):
        # data una coordinata inziale, restituisce una lista dei valori intorno alla coordinata data
        if 0 <= y <= self._rows and 0 <= x <= self._cols:
            element_around = []
            for i in self._d:
                x_n, y_n = i
                if 0 <= (y + y_n) <= self._rows - 1 and 0 <= (x + x_n) <= self._cols - 1:
                    element_around.append(self._board[(y + y_n) * self._cols + (x + x_n)])

            return element_around
        else:
            return False

    def search_coord_around(self, x, y, c):
        # data una coordinata e un valore, restituisce una lista di coordinate
        # del valori dato, intorno al punto di partenza
        if 0 <= y <= self._rows and 0 <= x <= self._cols:
            coord_element = []
            for i in self._d:
                x_n, y_n = i
                if 0 <= (y + y_n) <= self._rows - 1 and 0 <= (x + x_n) <= self._cols - 1:
                    if self._board[(y + y_n) * self._cols + (x + x_n)] == c:
                        coord_element.append(((x + x_n), (y + y_n)))
            return coord_element

    def insert_around(self, x, y, c):
        # inserisce un valore in una coordinata data
        if 0 <= y <= self._rows and 0 <= x <= self._cols:
            self._board[y * self._cols + x] = c

    def auto(self, x: int, y: int):
        # automatismi

        if self.control(x, y, "+"):
            # Autocompletamento, al click su un incrocio (+)
            element_around = self.search_element_around(x, y)
            number_element = element_around.count("|")
            if number_element == 2:
                # ci sono già due linee → tutte ×
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "x")

            # manca solo una casella → linea o ×
            if element_around.count(" ") == 1 and element_around.count("x") == 3:
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "|")

            elif element_around.count(" ") == 1 and element_around.count("|") == 3:
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "x")


        elif 48 <= ord(self._board[y * self._cols + x]) <= 57:
            # Autocompletamento, al click su un vincolo numerico
            number = self._board[y * self._cols + x]
            element_around = self.search_element_around(x, y)
            number_element = element_around.count("|")

            if number_element == int(number):
                # ci sono già le linee giuste → tutte ×
                list_coord = self.search_coord_around(x, y, " ")
                for coord in list_coord:
                    self.insert_around(*coord, "x")

            elif number_element <= int(number):
                # mancano n linee e ci sono n caselle libere → tutte linee
                list_element = self.search_element_around(x, y)
                list_coord = self.search_coord_around(x, y, " ")
                
                cont_x = list_element.count("x")
                cont_void = list_element.count(" ")
                if (cont_x <= int(number)) and (cont_void <= int(number) ): 
                
                    for coord in list_coord:
                        self.insert_around(*coord, "|")

    # contare le linee bene

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
        cont_line = 0
        self._num_line_loop = 0
        start_coord = (x, y)
        control = "+"
        # ricerca del single loop
        for i in range(self._num_line):
            tot_line = self._board.count("|")

            if (y < self._rows - 1) and (self._board[(y + 1) * self._cols + (x)] == control) and (
                    x != old_x or (y + 1) != old_y):
                old_x, old_y = x, y  # memorizzo la vecchia posizione
                if self.control(x, y, "|"):  # controllo se nella posizione x, y c'è una linea
                    cont_line += 1
                x, y = (x, y + 1)

            elif (y > 0) and (self._board[(y - 1) * self._cols + (x)] == control) and (x != old_x or (y - 1) != old_y):
                old_x, old_y = x, y
                if self.control(x, y, "|"):
                    cont_line += 1
                x, y = (x, y - 1)

            elif (x < self._cols - 1) and (self._board[(y) * self._cols + (x + 1)] == control) and (
                    (x + 1) != old_x or y != old_y):
                old_x, old_y = x, y
                if self.control(x, y, "|"):
                    cont_line += 1
                x, y = (x + 1, y)

            elif (x > 0) and (self._board[(y) * self._cols + (x - 1)] == control) and ((x - 1) != old_x or y != old_y):
                old_x, old_y = x, y

                if self.control(x, y, "|"):
                    cont_line += 1
                x, y = (x - 1, y)

            # cambio il valore di ricerca
            if control == "|":
                control = "+"
            elif control == "+":
                control = "|"

            # se le coordinate sono uguali a quelle iniziali (sono arrivato al punto di paretnza, ho un percorso chiuso)
            if (x, y) == start_coord:
                if tot_line == cont_line:
                    return True
        return False

    def control_plus(self):
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]

                if val == "+":
                    number_element = 0
                    element = self.search_element_around(x, y)
                    number_element = element.count("|")
                    if not (number_element == 2 or number_element == 0):
                        return False
        return True

    def finished(self) -> bool:
        # funzione di verfica vincita del gicoco
        count_true = 0
        # controllo che ad ogni numero ci sia il numero giusto di linee
        for x in range(self._cols):
            for y in range(self._rows):
                val = self._board[y * self._cols + x]
                # controllo ai segni + devono esserci 2 o 0 linee
                if "0" <= val < "4":
                    numbers_line = 0
                    numbers_element = self.search_element_around(x, y)
                    numbers_line = numbers_element.count("|")

                    if numbers_line == int(val):
                        count_true += 1

        # controllo condizioni di vittoria
        if self.control_loop():
            if (count_true == self._tot_num and self.control_plus()):
                return True
        else:
            return False

    def unsolvable(self):
         
         for x in range(self._cols):
            for y in range(self._rows):
            
                if "0" < (self._board[y * self._cols + x]) <= "3":
                     number = self._board[y * self._cols + x]
                     numbers_element = self.search_element_around(x, y)
                     number_x = numbers_element.count("x")
                     numer_line = numbers_element.count("|")
                     if not(number_x <= int(number) and numer_line <= int(number)):
                        return False
                
                
                if self.control(x, y, "+"):
                    plus_element = self.search_element_around(x, y)
                    plus_x = plus_element.count("x")
                    plus_line = plus_element.count("|")
                    
                    if not((plus_x == 0 or plus_x == 2) and (plus_line == 0 or  plus_line == 2)):
                        return False
                
            
    
         if self.control_loop():
             return True

         return False
         
                   
class BoardGameGui:
    def __init__(self, g: Slitherlink):
        self._game = g
        self._mouse_down = 0
        self._prev_keys = set()
        self._key = False
        self._game_menu = False
        self._solution = False

        self.update_buttons()

    def home_screen(self):
        solution = False
        #creazione della schermata di home
       
        g2d.draw_image("home.png", (0, 0))
        
        if(g2d.key_pressed("x")): 
           self._key = True
           self.update_buttons()

    def game_menu(self):
        if not(self._solution):
            g2d.draw_image("mode.png", (0, 0))

        if(g2d.key_pressed("1")): 
            self._game._game_mode1 = "game_nowin_5x5.txt"
            self._game.__init__(self._game._game_mode1)
            self._game_menu = True
            self.update_buttons()

        elif(g2d.key_pressed("2")):
            self._game._game_mode1 = "facile.txt"
            self._game.__init__(self._game._game_mode1)
            self._game_menu = True
            self.update_buttons()

        elif(g2d.key_pressed("3")):
            self._game._game_mode1 = "medio.txt"
            self._game.__init__(self._game._game_mode1)
            self._game_menu = True
            self.update_buttons()

        elif(g2d.key_pressed("4")):
            self._game._game_mode1 = "difficile.txt"
            self._game.__init__(self._game._game_mode1)
            self._game_menu = True
            self.update_buttons()
        
        else:
            self._game_menu = False
            

    def tick(self):

        if not (self._key):
            self.home_screen()

        if(self._key):
            if not(self._game_menu):
                self.game_menu()
            if (self._game_menu):
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

                if g2d.key_pressed("u"):
                    print(self._game.unsolvable())

                if g2d.key_pressed("m"):
                    self._game_menu = False
                    
                self._prev_keys = keys
                #self._game.control_loop()  # CANCELLARE
            

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
                if value == "|" or value == "-":
                    g2d.set_color((0,0,0))
                    if value == "-":
                        g2d.fill_rect(((x*40-20-1), (y*40 +20)), (80, 2))
                    elif value == "|":
                        g2d.fill_rect(((x*40+20-1), (y*40 -20)), (2, 80))
                elif "0" < value < "4":
                        numbers_line = 1
                        numbers_element = self._game.search_element_around(x,  (rows - y) - 1)
                        numbers_line = numbers_element.count("|")

                        if numbers_line == int(value):
                            g2d.set_color((0,230,0))
                            g2d.draw_text_centered(value, center, H // 2)
                        else:
                            g2d.set_color((0,0,0))
                            g2d.draw_text_centered(value, center, H // 2)
                else:
                    g2d.set_color((0,0,0))
                    g2d.draw_text_centered(value, center, H // 2)
                    
                
        if self._game.finished():
            g2d.draw_image("won.png", (0, 0))
            print("won")
           

def gui_play(game: Slitherlink):

        g2d.init_canvas((game.cols() * W, game.rows() * H))
        print("taglia", game.cols() * W, game.rows() * H)
        ui = BoardGameGui(game)
        g2d.main_loop(ui.tick)


s = Slitherlink("game_nowin_5x5.txt")
gui_play(s)