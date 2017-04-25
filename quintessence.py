import Tkinter as tk


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=24, columns=24, size=36, color1="antique white", color2="saddle brown"):

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.p1_pieces = []
        self.p2_pieces = []
        self.selected = None
        self.grid_steps = self.calculate_grid()
        print self.grid_steps

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")

        self.canvas.bind("<Configure>", self.refresh)

        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

    def calculate_grid(self):
        return [(n * self.size) for n in range(self.rows + 1)]

    def callback(self, event, board):
        if not board.selected:
            pieces = board.p1_pieces + board.p2_pieces
            for piece in pieces:
                if abs(piece.column - event.x) < 20 and abs(piece.row - event.y) < 20:
                    board.selected = piece
                    break
        elif board.selected:
            for n in range(len(board.grid_steps)):
                if event.x < board.grid_steps[n]:
                    print "column is %d" % n
                    board.selected.grid_col = n
                    board.selected.column = board.grid_steps[n] - board.size / 2
                    break
            for n in range(len(board.grid_steps)):
                if event.y < board.grid_steps[n]:
                    print "row is %d" % n
                    board.selected.grid_row = n
                    board.selected.row = board.grid_steps[n] - board.size / 2
                    break            
            if board.selected.move():
                board.selected = None

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
    def __init__(self, player, name, element, board):
        starting_positions = {"p1_air": 6, "p1_fire": 11, "p1_water": 16,
                              "p1_earth": 21, "p2_air": 21, "p2_fire": 16,
                              "p2_water": 11, "p2_earth": 6}
        self.player = player
        self.name = name
        self.element = element
        self.board = board
        self.image = tk.PhotoImage(file="%s.gif" % element)
        self.board.canvas.create_image(0,0, image=self.image, tags=(name, "piece"), anchor="c")
        self.grid_row = starting_positions[self.name]
        if player == "one":
            self.grid_col = 1
            self.board.p1_pieces.append(self) 
        else:
            self.grid_col = self.board.rows
            self.board.p2_pieces.append(self)   
        self.move()



    def move(self):
        # if self.element == "air":
        #     if abs(column - self.column) <= self.board.size * 4 and abs(row - self.row) < 20:
        #         self.row = row
        #         self.column = column
        #         self.board.canvas.coords(self.name, column, row)
        #         return True
        #     else:
        #         return False
        self.row = self.board.grid_steps[self.grid_row] - self.board.size / 2
        self.column = self.board.grid_steps[self.grid_col] - self.board.size / 2
        self.board.canvas.coords(self.name, self.column, self.row)
        return True


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    p1_air = Piece("one", "p1_air", "air", board)
    p1_fire = Piece("one", "p1_fire", "fire", board)
    p1_water = Piece("one", "p1_water", "water", board)
    p1_earth = Piece("one", "p1_earth", "earth", board)

    p2_air = Piece("two", "p2_air", "air", board)
    p2_fire = Piece("two", "p2_fire", "fire", board)
    p2_water = Piece("two", "p2_water", "water", board)
    p2_earth = Piece("two", "p2_earth", "earth", board)

    board.canvas.bind("<Button-1>", lambda event, arg=board: board.callback(event, arg))

    root.mainloop()
