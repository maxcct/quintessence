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
        self.grid_steps = [(n * size) - n for n in range(rows + 1)]
        print self.grid_steps

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")

        self.canvas.bind("<Configure>", self.refresh)

        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

    def callback(self, event, board):
        if not board.selected:
            pieces = board.p1_pieces + board.p2_pieces
            for piece in pieces:
                if abs(piece.column - event.x) < 20 and abs(piece.row - event.y) < 20:
                    print event.x
                    for n in range(len(board.grid_steps)):
                        if event.x < board.grid_steps[n]:
                            print "column is %d" % n
                            break
                    for n in range(len(board.grid_steps)):
                        if event.y < board.grid_steps[n]:
                            print "row is %d" % n
                            break
                    board.selected = piece
        elif board.selected:
            if board.selected.move(event.y, event.x):
                board.selected = None

    def refresh(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
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
            piece.move(piece.row, piece.column)
        for piece in self.p1_pieces:
            piece.move(piece.row, piece.column)
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


class Piece(object):
    def __init__(self, player, name, element, board):
        starting_positions = {"p1_air": 5.48, "p1_fire": 2.598, "p1_water": 1.7,
                              "p1_earth": 1.265, "p2_air": 1.265, "p2_fire": 1.7,
                              "p2_water": 2.598, "p2_earth": 5.48}
        self.player = player
        self.name = name
        self.element = element
        self.board = board
        self.image = tk.PhotoImage(file="%s.gif" % element)
        self.board.canvas.create_image(0,0, image=self.image, tags=(name, "piece"), anchor="c")
        self.row = (self.board.size * self.board.rows) / starting_positions[name]
        if player == "one":
            self.column = int(self.board.size / 2)
            self.board.p1_pieces.append(self) 
        else:
            self.column = (22.4 * self.board.size) + int(self.board.size / 2)
            self.board.p2_pieces.append(self)   
        self.board.canvas.coords(self.name, self.column, self.row)

    def move(self, row, column):
        if self.element == "air":
            if abs(column - self.column) <= self.board.size * 4 and abs(row - self.row) < 20:
                self.row = row
                self.column = column
                self.board.canvas.coords(self.name, column, row)
                return True
            else:
                return False
        self.row = row
        self.column = column
        self.board.canvas.coords(self.name, column, row)
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
