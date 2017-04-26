import Tkinter as tk


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=24, columns=24, size=36, color1="antique white", color2="saddle brown", turn="one"):

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.p1_pieces = []
        self.p2_pieces = []
        self.selected = None
        self.grid_steps = self.calculate_grid()
        self.turn = turn

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

    def calculate_grid(self):
        return [(n * self.size) for n in range(self.rows + 1)]

    def click(self, event, board):
        if board.turn == "one":
            pieces = board.p1_pieces
        else:
            pieces = board.p2_pieces
        for piece in pieces:
            if abs(piece.column - event.x) < 20 and abs(piece.row - event.y) < 20:
                board.selected = piece
                return
        if board.selected:
            target_column = None
            target_row = None
            for n in range(len(board.grid_steps)):
                if not target_column or not target_row:
                    if not target_column and event.x < board.grid_steps[n]:
                        print "column is %d" % n
                        target_column = n
                    if not target_row and event.y < board.grid_steps[n]:
                        print "row is %d" % n
                        target_row = n
                else:
                    break
            if board.selected.validate_move(target_column, target_row):
                board.selected.grid_col = target_column
                board.selected.grid_row = target_row
                board.selected.move()
                self.end_turn()

    def up(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "up"
                self.end_turn()

    def right(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "right"
                self.end_turn()

    def down(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "down"
                self.end_turn()

    def left(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "left"
                self.end_turn()


    def end_turn(self):
            board.selected = None
            board.turn = "two" if board.turn == "one" else "one"        

    def refresh(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.grid_steps = self.calculate_grid()
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for piece in self.p2_pieces:
            piece.move()
        for piece in self.p1_pieces:
            piece.move()
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


class Piece(object):
    def __init__(self, element, player, board):
        self.player = player
        self.board = board
        self.element = element
        self.image = tk.PhotoImage(file="%s.gif" % element)
        self.name = element + "_" + player
        self.board.canvas.create_image(0,0, image=self.image, tags=(self.name, "piece"), anchor="c")
        if player == "one":
            self.grid_col = 1
        else:
            self.grid_col = self.board.rows

    def move(self):
        self.row = self.board.grid_steps[self.grid_row] - self.board.size / 2
        self.column = self.board.grid_steps[self.grid_col] - self.board.size / 2
        self.board.canvas.coords(self.name, self.column, self.row)
        return True


class Air(Piece):
    def __init__(self, player, board):
        Piece.__init__(self, "air", player, board)
        if player == "one":
            self.direction = "right"
            self.grid_row = 5
            self.board.p1_pieces.append(self) 
        else:
            self.direction = "left"
            self.grid_row = 20
            self.board.p2_pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        if self.direction == "right" or self.direction == "left":
            if abs(self.grid_col - column) <= 5 and abs(self.grid_row - row) == 0:
                return True
        elif self.direction == "up" or self.direction == "down":
            if abs(self.grid_row - row) <= 5 and abs(self.grid_col - column) == 0:
                return True
        else:
            return False

class Fire(Piece):
    def __init__(self, player, board):
        Piece.__init__(self, "fire", player, board)
        if player == "one":
            self.grid_row = 10
            self.board.p1_pieces.append(self) 
        else:
            self.grid_row = 15
            self.board.p2_pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        if abs(self.grid_col - column) == 1 and abs(self.grid_row - row) == 0:
            return True
        elif abs(self.grid_col - column) == 2 and abs(self.grid_row - row) <= 1:
            return True
        elif abs(self.grid_col - column) == 3 and abs(self.grid_row - row) <= 2:
            return True
        else:
            return False

class Water(Piece):
    def __init__(self, player, board):
        Piece.__init__(self, "water", player, board)
        if player == "one":
            self.grid_row = 15
            self.board.p1_pieces.append(self) 
        else:
            self.grid_row = 10
            self.board.p2_pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        movement = column - self.grid_col
        if self.player == "two":
            movement = 0 - movement
        if movement <= 3 and movement > 0 and abs(self.grid_row - row) <= 1:
            return True
        else:
            return False

class Earth(Piece):
    def __init__(self, player, board):
        Piece.__init__(self, "earth", player, board)
        if player == "one":
            self.grid_row = 20
            self.board.p1_pieces.append(self) 
        else:
            self.grid_row = 5
            self.board.p2_pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        if abs(self.grid_col - column) <= 1 and abs(self.grid_row - row) <= 1:
            return True
        else:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    p1_air = Air("one", board)
    p1_fire = Fire("one", board)
    p1_water = Water("one", board)
    p1_earth = Earth("one", board)

    p2_air = Air("two", board)
    p2_fire = Fire("two", board)
    p2_water = Water("two", board)
    p2_earth = Earth("two", board)

    board.canvas.bind("<Button-1>", lambda event, arg=board: board.click(event, arg))
    board.canvas.bind("<Up>", lambda event, arg=board: board.up(event, arg))
    board.canvas.bind("<Right>", lambda event, arg=board: board.right(event, arg))
    board.canvas.bind("<Down>", lambda event, arg=board: board.down(event, arg))
    board.canvas.bind("<Left>", lambda event, arg=board: board.left(event, arg))
    board.canvas.focus_set()

    root.mainloop()
