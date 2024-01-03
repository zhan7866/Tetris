import turtle, random

SCALE = 32 # controls how many pixels wide each grid square is

rows = 20
cols = 10

class Game:
    def __init__(self):
 
        # turtle = turtle.Turtle()
        self.score_turtle = turtle.Turtle()
        turtle.setup(SCALE*12+20, SCALE*22+20)

        turtle.setworldcoordinates(-1.5, -2.5, 10.5, 23.5)
        cv = turtle.getcanvas()
        cv.adjustScrolls()

        turtle.hideturtle()
        turtle.delay(0)
        turtle.speed(0)
        turtle.tracer(0, 0)

        # rectangular game area, height = 20, width = 10
        turtle.bgcolor('black')
        turtle.pencolor('white')
        turtle.penup()
        turtle.setpos(-0.525, -0.525)
        turtle.pencolor("white")
        turtle.pendown()
        for i in range(2):
            turtle.forward(10.05)
            turtle.left(90)
            turtle.forward(20.05)
            turtle.left(90)
        
        turtle.penup()
        turtle.goto(1.5, 22)
        turtle.pencolor("ivory")
        turtle.pendown()
        turtle.forward(6)
        turtle.right(90)
        turtle.forward(1.5)
        turtle.right(90)
        turtle.forward(6)
        turtle.right(90)
        turtle.forward(1.5)

        self.score = 0

        self.write("Score:", 3, 21.05, "Impact", "ivory", 10)

        self.write_score()

        self.write("Paulina's Tetris Game", 4.5, 22.5, "Copperplate", "rosy brown", 20)


        self.occupied = {} # None if not occupied --> replace w Square when occupied
        for i in range(20):
            for j in range(10):
                self.occupied[j,i] = None
        print(self.occupied)

        self.active = Block()
    
        self.gameloop()

        turtle.onkeypress(self.move_left, 'Left')
        turtle.onkeypress(self.move_right, 'Right')
        turtle.onkeypress(self.move_down, "Down")
        turtle.onkeypress(self.rotate, "space")

        turtle.update()
        turtle.listen()
        turtle.mainloop()

    def write_score(self):
        self.score_turtle.clear()
        self.score_turtle.penup()
        self.score_turtle.goto(5, 21.05)
        self.score_turtle.pendown()
        self.score_turtle.pencolor("ivory")
        self.score_turtle.write(self.score, align="center", font=("Impact", 10, "bold"))
        self.score_turtle.penup()
    def gameloop(self):
        if self.active.valid(0, -1, self.occupied):
            self.active.move(0, -1)
        else:
            for square in self.active.squares:
                self.occupied[square.xcor(), square.ycor()] = square
            self.eliminate()
            if not self.game_over():
                self.active = Block()
        turtle.update()
        turtle.ontimer(self.gameloop, 300)
    def eliminate(self):
        index = 0
        while index < rows:
            if all(self.occupied[col, index] for col in range(cols)):
                self.eliminate_row(index)
                turtle.update()
            else:
                index += 1

    def eliminate_row(self, row):
        # if all(self.occupied[col, row] for col in range(cols)):
        # dict = {}
        # for i in range(rows):
        #     dict[rows] = 0

        # ^ using for debug 
            
        for i in range(row, rows - 1):
            for col in range(cols):
                if self.occupied[col, i + 1]:
                    # dict[col] = row
                    self.occupied[col, i + 1].move(col, i)
                self.occupied[col, i] = self.occupied[col, i + 1]
                self.occupied[col, i + 1] = None

        for col in range(cols):
            if self.occupied[col, rows - 1]:
                self.occupied[col, rows - 1].clear()
                self.occupied[col, rows - 1].hideturtle()
                Square(col, rows-1, "black")
                self.occupied[col, rows - 1] = None

        self.score += 100
        self.write_score()
        turtle.update()
    def move_left(self):
        if self.active.valid(-1, 0, self.occupied):
            self.active.move(-1, 0)
            turtle.update()
    def move_right(self):
        if self.active.valid(1, 0, self.occupied):
            self.active.move(1, 0)
            turtle.update()
    def move_down(self):
        while self.active.valid(0, -1, self.occupied):
            self.active.move(0, -1)
            turtle.update()
    def write(self, message, x, y, font, color, size):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.pencolor(color)
        turtle.write(message, align="center", font=(font, size, "bold"))
    def game_over(self):  
        for square in self.active.squares:
            if square.ycor() >= 19:
                self.write("GAME OVER :)", 4.5, 10, "Copperplate", "white", 40)
                return True
        return False
    def rotate(self):
        if self.active.rotate(self.occupied):
            turtle.update()



        
class Square(turtle.Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.shape('square')
        self.shapesize(SCALE/20)
        self.speed(20)
        self.fillcolor(color)
        self.pencolor('gray')
        self.penup()
        self.goto(x, y)
    def move(self, x, y):
        self.goto(x, y)

class Block:
    def __init__(self):
        self.squares = []
        self.sq_dict = {1:[Square(3,25,'light cyan'), Square(4,25,'light cyan'), Square(5,25,'light cyan'), Square(6,25,'light cyan')], 
            2:[Square(3,26, 'sky blue'), Square(3,25,'sky blue'), Square(4,25,'sky blue'), Square(5,25,'sky blue')], 
            3:[Square(4,25,'light salmon'), Square(5,25,'light salmon'), Square(6,25,'light salmon'), Square(6,26,'light salmon')], 
            4:[Square(4,25,'tan'), Square(4,26,'tan'), Square(5,25,'tan'), Square(5,26,'tan')], 
            5:[Square(3,25,'aquamarine'), Square(4,25,'aquamarine'), Square(4,26,'aquamarine'), Square(5,26,'aquamarine')], 
            6:[Square(3,25,'lavender'), Square(4,25,'lavender'), Square(4,26,'lavender'), Square(5,25,'lavender')], 
            7:[Square(3,26,'light coral'), Square(4,26,'light coral'), Square(4,25,'light coral'), Square(5,25,'light coral')]}
        self.shape = random.randint(1,7)
        # print(self.shape)
        for i in self.sq_dict[self.shape]:
            self.squares.append(i)
    def move(self, dx, dy):
        for square in self.squares:
            square.goto(square.xcor() + dx, square.ycor() + dy)
    def valid(self, dx, dy, occ):
        for square in self.squares:
            if not (0 <= square.xcor() + dx <= 9 and 0 <= square.ycor() + dy): # check if this works
                print(square.xcor(), square.ycor())
                return False
            if square.ycor() + dy < 19 and occ[square.xcor() + dx,square.ycor() + dy]:
                return False
        return True
    def rotate(self, occupied):
        temp = []

        for square in self.squares:
            relative_x = square.xcor() - self.squares[0].xcor()
            relative_y = square.ycor() - self.squares[0].ycor()
            new_x = round(self.squares[0].xcor() - relative_y)
            new_y = round(self.squares[0].ycor() + relative_x)

            temp.append((new_x, new_y))

        for new_x, new_y in temp:
            if not self.valid(new_x - self.squares[0].xcor(), new_y - self.squares[0].ycor(), occupied):
                return False

        for square in self.squares:
            square.clear()

        for i, square in enumerate(self.squares):
            square.move(temp[i][0], temp[i][1])

        return True




if __name__ == '__main__':
    temp = Game()

    # find a way to implement play again button ._.


# https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/