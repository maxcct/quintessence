import Tkinter as tk
# import random


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=24, columns=24, size=36, color1="AntiqueWhite1", color2="AntiqueWhite2", turn="one"):

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = []
        self.player_one_pieces = {"air": 0, "fire": 0, "water": 0, "earth": 0}
        self.player_two_pieces = {"air": 0, "fire": 0, "water": 0, "earth": 0}
        self.positions = [[None for n in range(columns)] for n in range(rows)]
        self.selected = None
        self.grid_steps = self.calculate_grid()
        self.turn = turn
        self.turn_status = tk.Label(root, text="It is player %s's turn" % self.turn)
        # self.failed = None
        self.victory = None
        self.gameover_status = False

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.turn_status.pack()

    def calculate_grid(self):
        return [(n * self.size) for n in range(self.rows+1)]

    def set_positions(self):
        for piece in self.pieces:
            self.positions[piece.grid_row-1][piece.grid_col-1] = piece

    def convert_coords(self, event):
        target_column = None
        target_row = None
        for n in range(len(board.grid_steps)):
            if not target_column or not target_row:
                if not target_column and event.x < board.grid_steps[n]:
                    target_column = n
                if not target_row and event.y < board.grid_steps[n]:
                    target_row = n
            else:
                break
        return (target_column, target_row)        

    def click(self, event, board):
        # if board.failed:
        #     board.failed.pack_forget()
        target = board.convert_coords(event)
        if not target[0] or not target[1]:
            return
        target_column = target[0]
        target_row = target[1]
        target_piece = board.positions[target_row-1][target_column-1]
        if target_piece and not board.selected and board.turn == target_piece.player:
            board.selected = target_piece
            return
        elif board.selected:
            if target_piece:
                # if board.selected.element == "air":
                #     if target_piece.element not in board.selected.prey:
                #         return
                if target_piece.element != board.selected.prey:
                    return
                elif target_piece.grid_col == 1 or target_piece.grid_col == board.rows:
                    return
            if board.selected.validate_move(target_column, target_row):
                board.selected.remove_last_position()
                board.selected.grid_col = target_column
                board.selected.grid_row = target_row
                game_continue = board.selected.move()
                if game_continue:
                    board.end_turn()

    def up(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "up"
                board.end_turn()
            elif board.selected.element == "water":
                board.selected.direction = "diagonal_up"
                board.end_turn()

    def right(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "right"
                board.end_turn()
            elif board.selected.element == "water" and board.selected.player == "one":
                board.selected.direction = "lateral"
                board.end_turn()

    def down(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "down"
                board.end_turn()
            elif board.selected.element == "water":
                board.selected.direction = "diagonal_down"
                board.end_turn()

    def left(self, event, board):
        if board.selected:
            if board.selected.element == "air":
                board.selected.direction = "left"
                board.end_turn()
            elif board.selected.element == "water" and board.selected.player == "two":
                board.selected.direction = "lateral"
                board.end_turn()

    def end_turn(self):
        self.selected = None
        self.turn = "two" if self.turn == "one" else "one"
        self.turn_status["text"] = "It is player %s's turn" % self.turn
        self.turn_status.pack()

    def gameover(self, victor):
        self.gameover_status = True
        self.turn_status.pack_forget()
        self.victory = tk.Label(root, text="Player %s wins!" % victor.player)
        self.victory.pack()

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
        for piece in self.pieces:
            piece.move()
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


class Piece(object):
    def __init__(self, element, player, board, row):
        self.player = player
        self.board = board
        self.element = element
        self.image = tk.PhotoImage(file="%s_%s.gif" % (element, player))
        self.name = str(row) + "_" + element + "_" + player
        self.board.canvas.create_image(0,0, image=self.image, tags=(self.name, "piece"), anchor="c")
        self.grid_row = row
        if player == "one":
            self.grid_col = 1
            self.board.player_one_pieces[element] += 1
        else:
            self.grid_col = self.board.rows
            self.board.player_two_pieces[element] += 1

    def remove_last_position(self):
        self.board.positions[self.grid_row-1][self.grid_col-1] = None

    def move(self):
        self.row = self.board.grid_steps[self.grid_row] - self.board.size / 2
        self.column = self.board.grid_steps[self.grid_col] - self.board.size / 2
        self.board.canvas.coords(self.name, self.column, self.row)
        self.board.positions[self.grid_row-1][self.grid_col-1] = self
        if self.board.gameover_status:
            return False
        elif self.check_for_victory():
            self.board.gameover(self)
            return False
        return True

    def attack(self, column, row):
        target_piece = self.board.positions[row-1][column-1]
        if target_piece:
            if target_piece.element == self.prey:
                return self.destroy(target_piece)
            else:
                return False
        return True

    def destroy(self, target):
        target.remove_last_position()
        self.board.pieces.remove(target)
        self.board.canvas.delete(target)
        if target.player == "one":
            self.board.player_one_pieces[target.element] -= 1
            if self.board.player_one_pieces[target.element] == 0:
                self.board.gameover(self)
        elif target.player == "two":
            self.board.player_two_pieces[target.element] -= 1
            if self.board.player_two_pieces[target.element] == 0:
                self.board.gameover(self)
        del target
        return True         

    def check_for_victory(self):
        column_to_check = 0
        if ((self.grid_col == self.board.columns and self.player == "one")
           or (self.grid_col == 1 and self.player == "two")):
            column_to_check = self.grid_col
        if column_to_check:
            elements = []
            for row in self.board.positions:
                at_column = row[column_to_check-1]
                if at_column:
                    if at_column.player == self.player:
                        elements.append(at_column.element)
            if ("air" in elements and "fire" in elements and "water"
                in elements and "earth" in elements):
                return True
        return False


class Air(Piece):
    def __init__(self, player, board, row):
        Piece.__init__(self, "air", player, board, row)
        if player == "one":
            self.direction = "right"
        else:
            self.direction = "left"
        self.prey = "water"
        self.board.pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        if self.direction == "right" or self.direction == "left":
            movement = column - self.grid_col
            if self.direction == "left":
                movement = 0 - movement
            if movement <= 5 and movement > 0 and abs(self.grid_row - row) == 0:
                return self.attack(column, row)
        elif self.direction == "up" or self.direction == "down":
            movement = row - self.grid_row
            if self.direction == "up":
                movement = 0 - movement
            if movement <= 5 and movement > 0 and abs(self.grid_col - column) == 0:
                return self.attack(column, row)
        return False

    # def attack(self, column, row):
    #     target_piece = self.board.positions[row-1][column-1]
    #     if target_piece:
    #         if random.random() > 0.5:
    #             return self.destroy(target_piece)
    #         else:
    #             self.board.failed = tk.Label(root, text="The wind did not blow strongly enough")
    #             self.board.failed.pack()
    #             self.board.end_turn()
    #             return False
    #     return True


class Fire(Piece):
    def __init__(self, player, board, row):
        Piece.__init__(self, "fire", player, board, row)
        self.prey = "earth"
        self.board.pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        col_movement = self.grid_col - column
        row_movement = self.grid_row - row
        if self.player == "one":
            col_movement = 0 - col_movement
        if col_movement <= 3 and col_movement > 0 and row_movement == 0:
            return self.attack(column, row)
        elif col_movement == 2 and abs(row_movement) <= 1:
            return self.attack(column, row)
        elif col_movement == 3 and abs(row_movement) <= 2:
            return self.attack(column, row)
        return False


class Water(Piece):
    def __init__(self, player, board, row):
        Piece.__init__(self, "water", player, board, row)
        self.direction = "lateral"
        self.prey = "fire"
        self.board.pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        row_move = row - self.grid_row
        col_move = column - self.grid_col
        if self.player == "two":
            col_move = 0 - col_move
        if self.direction == "lateral":
            if col_move <= 3 and col_move > 0 and abs(row_move) <= 1:
                return self.attack(column, row)
        elif self.direction == "diagonal_up" or self.direction == "diagonal_down":
            if self.direction == "diagonal_up":
                row_move = 0 - row_move
            if col_move >= 0 and col_move <= 3 and row_move >= 0 and row_move <= 3:
                if row_move == 1 or row_move == 2 and col_move == 0:
                    return self.attack(column, row)
                elif (col_move <= 2 and row_move == 0) or (col_move <= 3 and row_move > 0):
                    return self.attack(column, row)
        else:
            return False


class Earth(Piece):
    def __init__(self, player, board, row):
        Piece.__init__(self, "earth", player, board, row)
        self.prey = "air"
        self.board.pieces.append(self)
        self.move()

    def validate_move(self, column, row):
        if abs(self.grid_col - column) <= 2 and abs(self.grid_row - row) <= 2:
            return self.attack(column, row)
        else:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    for n in range(1, board.rows+1):
        if n == 2 or n == 10 or n == 18:
            Air("one", board, n)
        elif n == 1 or n == 9 or n == 17:
            Earth("two", board, n)
        elif n == 8 or n == 16 or n == 24:
            Earth("one", board, n)
        elif n == 3 or n == 11 or n == 19:
            Water("two", board, n)
        elif n == 4 or n == 12 or n == 20:
            Fire("one", board, n)
        elif n == 5 or n == 13 or n == 21:
            Fire("two", board, n)
        elif n == 6 or n == 14 or n == 22:
            Water("one", board, n)
        elif n == 7 or n == 15 or n == 23:
            Air("two", board, n)

    board.set_positions()

    board.canvas.bind("<Button-1>", lambda event, arg=board: board.click(event, arg))
    board.canvas.bind("<Up>", lambda event, arg=board: board.up(event, arg))
    board.canvas.bind("<Right>", lambda event, arg=board: board.right(event, arg))
    board.canvas.bind("<Down>", lambda event, arg=board: board.down(event, arg))
    board.canvas.bind("<Left>", lambda event, arg=board: board.left(event, arg))
    board.canvas.focus_set()

    root.mainloop()
