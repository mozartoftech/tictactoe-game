import random
import time
import sys

print("")

class Player:
    
    def __init__(self, letter):
        self.letter = letter 

    def cell_move(self, game):
        pass

class Random_Computer_Player(Player):
    
    def __init__(self, letter):
        super().__init__(letter) # the super method ensures that the letter attribute is set correctly for every instance of the sub-class.

    def cell_move(self, game): # game represents the current state of the Tictactoe game.
        
        cell = random.choice(game.available_cells())
        return cell

class Human_Player(Player):

    def __init__(self, letter):
        super().__init__(letter)

    def cell_move(self, game):
        
        cell_value = None # the user has not entered any value yet.
        valid_cell = False # let's assume that there are no valid cells
        
        while not valid_cell:
            
            cell = input(f"\n{self.letter}'s turn. Choose a cell from 0 to 8: ")

            try:
                cell_value = int(cell)
                
                if cell_value not in game.available_cells():
                    raise ValueError
                else: # if the cell_value is an index in game.available_cells.
                    valid_cell = True 
                
            except ValueError:
                print("Not a valid cell. Choose another.")
                
        return cell_value # this is only returned once a vaild square has been gotten.
        
        

class Tictactoe:

    def __init__(self):
        
        self.game_board = [] # creating the game board.
        for cells in range(9):
            cells = " "
            self.game_board.append(cells)

        self.current_winner = None

    def print_board(self):
        
        rows = []
        for i in range(3):
            row = self.game_board[i * 3 : (i + 1) * 3] # this creates a sublist 
            rows.append(row)
        for row in rows:  # iterating through the rows and modifying it.
            modify_board = f"| {' | '.join(row)} |" 
            print(modify_board)

    @staticmethod 
    def print_guide_board(): # guides the player on how to make a move based on the index of the cell
        
        number_list = [] # stores the rows of the board as sublists
        
        for j in range(3): # the iterator "j" iterates from 0 to 2
            # for each value of j:
            row = [] # holds the rows which are added to the "number_list" list after each iteration
            
            for i in range((j * 3), (j + 1) * 3):
                i = str(i)
                row.append(i) # when j is 0, row appends 0, 1, 2 values of i.
            number_list.append(row)

        for row in number_list:
            print(f"| {' | '.join(row)} |")

    def empty_cells(self):
        
        emptycell = " " in self.game_board # if there is are quotation marks on the game board, it means that the cell is empty.
        return emptycell # returns a boolean value indicating if the cell is empty or not.

    def number_of_empty_cells(self):
        
        count_empty = self.game_board.count(" ")
        return count_empty

    def available_cells(self): # this method returns the cells that are available to make a move on.
        
        available = []

        for index, cell in enumerate(self.game_board): # the enumerate method returns a tuple of the index and the corresponding element in pairs. For each iteration, "index" represents the index of the current cell on the board, and "cell" represents the value of that cell.
            if cell == " ":
                available.append(index)
        return available

    def make_moves(self, cell, letter):
        
        if self.game_board[cell] == " ":
            self.game_board[cell] = letter
            if self.check_winner(cell, letter):
                self.current_winner = letter
            return True # indicates that the player made a valid move.
        
        return False # indicates that the move is invalid and was not made.

    def check_winner(self, cell, letter):

        # 3 in a row:
        row_index = cell // 3

        # constructing the row
        row = self.game_board[(row_index * 3): (row_index + 1) * 3]

        check_row = []

        for cells in row:
            # checks if the value of all cells in the row equals the player's letter. 
            check_row.append(cells == letter) # appends a boolean value since it checks if each cell in the row equals the player's letter
        if all(check_row) == True: # if all the boolean values in the check_row list equals true, then we return true
            return True 

        # 3 in a column:
        column_index = cell % 3 

        # constructing the column
        column = [] # holds the list of our column indices

        for i in range(3):
            col = self.game_board[column_index + (i * 3)]
            column.append(col)

        check_column = []

        for cells in column:
            check_column.append(cells == letter)

        if all(check_column) == True:
            return True

        # 3 in the diagonals

        if cell % 2 == 0:

            diagonal1 = []

            for i in [0, 4, 8]:
                diagonal = self.game_board[i]
                diagonal1.append(diagonal)

            check_diagonal1 = [] # checks if the diagonal has all letters the same.

            for cells in diagonal1:
                check_diagonal1.append(cells == letter) # appends a boolean value 

            if all(check_diagonal1) == True:
                return True
            
            diagonal2 = []

            for i in [2, 4, 6]:
                diagonal = self.game_board[i]
                diagonal2.append(diagonal)

            check_diagonal2 = [] # checks if the diagonal has all letters the same.

            for cells in diagonal2:
                check_diagonal2.append(cells == letter) # appends a boolean value 

            if all(check_diagonal2) == True:
                return True

        return False

def play_game(game, player_x, player_o, print_game = True):
    
    if print_game:
        game.print_guide_board()
    # starting letter 
    letter = "X"

    while game.empty_cells():
        if letter == "O":
            cell = player_o.cell_move(game)
        else:
            cell = player_x.cell_move(game)

        if game.make_moves(cell, letter): # Here we want to visualize our moves
            if print_game:
                print(f"\n{letter} moves to cell {cell}\n")
                game.print_board() # a new state of the board after a move has been made.
                print("") # just an empty line.  

            if game.current_winner: # This will run if it is no longer set to None, indicating that there is a winner
                if print_game:
                    print(f"{letter} wins the game!\n")
                return letter

            # after making our moves, we would need to alternate letters.
            if letter == "X":
                letter = "O"
            else:
                letter = "X"

        if print_game:
            time.sleep(1.5)

    if print_game:
        print("Tie game!")

if __name__ == "__main__":

    t = Tictactoe()

    while True:
        game_intro = input(f"This is my first tictactoe game! \nPlease choose a letter: ")

        if game_intro.lower() not in ["x", "o"]:
            print(f"\nChoose either X or O")
            continue
            
        elif game_intro.lower() == "x":
            player_x = Human_Player(game_intro.upper())
            player_o = Random_Computer_Player("O")

        else:
            player_x = Random_Computer_Player("X")
            player_o = Human_Player(game_intro.upper())
            
        
        play_game(t, player_x, player_o, print_game=True)

        while True:
            play_again = input("\nY for Yes or \nQ for Quit \n\n")
            
            if play_again.lower() not in ["y", "q"]:
                continue
            
            elif play_again.lower() == "y":
                t = Tictactoe()
                play_game(t, player_x, player_o, print_game=True)
                
            else:
                sys.exit()
        
    
        

