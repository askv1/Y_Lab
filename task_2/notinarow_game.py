import random
from turtle import Turtle, Screen
from itertools import product


FONT = ('Consolas', 16)


class Game:

    def __init__(self):

        self.board_xpos = -250
        self.board_ypos = -250
        self.cellsize = 50
        self.fig_rad = self.cellsize / 5
        self.n_turn = 0

        self.x_prev = 0
        self.y_prev = 0

        self.weights = [[self.cdist(i, j) for i in range(10)]
                        for j in range(10)]

        self.board = [['_'] * 10 for i in range(10)]

        self.next_turn = 'x'
        self.player_fig = random.choice('xo')

    def cdist(self, x, y):
        return ((x-4.5)**2 + (y-4.5)**2) ** 0.5

    def draw_line(self, x1, y1, x2, y2):

        self.pen.penup()
        self.pen.goto(x1, y1)
        self.pen.pendown()
        self.pen.goto(x2, y2)

    def draw_x(self, x, y):

        self.pen.width(3)
        self.draw_line(x-self.fig_rad, y-self.fig_rad,
                       x+self.fig_rad, y+self.fig_rad)
        self.draw_line(x-self.fig_rad, y+self.fig_rad,
                       x+self.fig_rad, y-self.fig_rad)
        self.pen.width(1)

    def draw_o(self, x, y):

        self.pen.width(3)
        self.pen.penup()
        self.pen.goto(x, y-self.fig_rad//2-4)
        self.pen.pendown()
        self.pen.circle(self.fig_rad)

    def draw_board(self):

        screen.bgcolor("yellow")
        screen.bgcolor()

        self.game_over = False

        self.msg = Turtle(visible=False)
        self.msg.speed(100)
        self.msg.penup()
        self.msg.goto(0, -300)

        self.pen = Turtle(visible=False)
        self.pen.speed(100)

        for i in range(11):

            self.draw_line(-self.board_xpos, (i-5)*self.cellsize,
                           self.board_xpos, (i-5)*self.cellsize)

            self.draw_line((i-5)*self.cellsize, -self.board_ypos,
                           (i-5)*self.cellsize, self.board_ypos)

        self.pen.forward(1)

        screen.onclick(lambda x, y: self.mouse_down(x, y))

        if self.next_turn != self.player_fig:
            self.ai_turn()

    def check_line(self, x, dx, y, dy):

        cons_count = 0

        while True:

            if self.board[x][y] == self.next_turn:
                cons_count += 1
            else:
                cons_count = 0 if cons_count < 5 else 5

            x += dx
            y += dy

            if x > 9 or y > 9:
                break

        return cons_count >= 5

    def check_loss(self, cellx, celly):

        row_count = 0
        col_count = 0

        h_loss = self.check_line(0, 1, celly, 0)
        v_loss = self.check_line(cellx, 0, 0, 1)

        diag_shift = min(cellx, 9 - celly)
        d1_loss = self.check_line(cellx-diag_shift, 1, celly+diag_shift, -1)

        diag_shift = min(cellx, celly)
        d2_loss = self.check_line(cellx-diag_shift, 1, celly-diag_shift, 1)

        return h_loss or v_loss or d1_loss or d2_loss

    def change_weights(self, cellx, celly):

        for i in range(1, 10, 1):

            for delta in product([-i, 0, i], repeat=2):

                dx = cellx+delta[0]
                dy = celly+delta[1]

                if (0 <= dx <= 9) and (0 <= dy <= 9) and (
                        self.board[dx][dy] == '_'):

                    if self.next_turn == self.player_fig:
                        self.weights[dx][dy] -= 1 / i
                    else:
                        self.weights[dx][dy] -= (30 // i)

    def ai_turn(self):

        potential_pos = []

        max_w = max(map(max, self.weights))

        for cellx in range(0, 10):
            for celly in range(0, 10):
                if self.weights[cellx][celly] == max_w:
                    potential_pos.append((cellx, celly))

        cellx, celly = random.choice(potential_pos)

        self.make_turn(cellx, celly)

    def make_turn(self, cellx, celly):

        if self.game_over:
            return

        x = self.board_xpos + (cellx + 0.5) * self.cellsize
        y = self.board_ypos + (celly + 0.5) * self.cellsize

        if self.next_turn != self.player_fig:
            self.pen.color('black')
            if self.n_turn > 2:
                if self.next_turn == 'x':
                    self.draw_x(self.x_prev, self.y_prev)
                else:
                    self.draw_o(self.x_prev, self.y_prev)
                self.pen.color('purple')
            self.x_prev = x
            self.y_prev = y
        else:
            self.pen.color('black')

        if self.next_turn == 'x':
            self.draw_x(x, y)
        else:
            self.draw_o(x, y)

        self.board[cellx][celly] = self.next_turn
        self.n_turn += 1

        if self.check_loss(cellx, celly):
            self.game_over = True
            if self.next_turn == self.player_fig:
                self.msg.write('AI has won!', align='center', font=FONT)
            else:
                self.msg.write('Player has won!', align='center', font=FONT)
        elif self.n_turn == 100:
            self.msg.write('Draw!', align='center', font=FONT)

        self.weights[cellx][celly] = -1e10
        self.change_weights(cellx, celly)

        self.next_turn = 'ox'['xo'.index(self.next_turn)]

    def mouse_down(self, x, y):

        if self.next_turn != self.player_fig:
            return

        cellx = int((x - self.board_xpos) // self.cellsize)
        celly = int((y - self.board_ypos) // self.cellsize)

        if not((0 <= cellx <= 9) and (0 <= celly <= 9)):
            return

        if self.board[cellx][celly] != '_':
            self.msg.write('Cell is blocked!', align='center', font=FONT)
            return
        else:
            self.msg.clear()

        self.make_turn(cellx, celly)

        self.ai_turn()


screen = Screen()
game = Game()
game.draw_board()
screen.mainloop()
