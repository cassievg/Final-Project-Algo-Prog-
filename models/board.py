import eel

from .exceptions import ChessException

from .gamepieces.king import King
from .gamepieces.rook import Rook

class EmptyCell:
    def __init__(self):
        self.symbol = ' '
        self.colour = ' '

# This class is responsible for the board that is being displayed
class BoardState:
    def __init__(self, board_simulation):
        self._board_simulation = board_simulation
        self.size = board_simulation.size
        # Positions in form of list of lists
        self.positions = [
            [
                EmptyCell()
                for y in range(self.size[1])
            ]
            for x in range(self.size[0])
        ]
    
    # To check if piece is in the board or in bounds
    def check_bounds(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return False
        else:
            return True
        
    # To check if board position (x, y) is empty
    def is_empty(self, x, y):
        return isinstance(self.positions[x][y], EmptyCell)

    # Combine both check_bounds and is_empty
    def is_empty_or_out_of_bounds(self, x, y):
        return not self.check_bounds(x, y) or self.is_empty(x, y)
    
    # Check if the piece at position (x, y) is a rook
    def is_rook(self, x, y):
        return isinstance(self.positions[x][y], Rook)
    
    # Show board
    def show(self):
        result = []

        # Goes through every position in the board and lists them down per row
        for row in self.positions:
            row_result = []

            # Takes the piece or empty cell in a row
            for unit in row:
                if isinstance(unit, EmptyCell):
                    row_result.append(None)
                else:
                    row_result.append({'type': 'piece', 'name': unit.__class__.__name__.lower(), 'colour': unit.colour})

            # After looping through each row, append each row list to result
            result.append(row_result)

        # Bring the result to the JQuery in the UI
        eel.show_board(result)()

    # To show all the possible moves of the selected piece
    def show_possible_moves(self, x, y):
        if not self.check_bounds(x, y):

            # Raise error if piece is out of bounds
            raise ChessException('This is not in the board.')
        
        elif isinstance(self.positions[x][y], EmptyCell):

            # Raise error if empty cell is selected
            raise ChessException('This is an empty cell.')
        
        else:

            # Takes the clean moves of the piece in position (x, y)
            possible_moves = self.positions[x][y].get_clean_moves(self._board_simulation, x, y)

            result = []

            # Loop to check every position in the board
            for i, unit_list in enumerate(self.positions):
                row_result = []
                for j, unit in enumerate(unit_list):

                    # If the position is in the possible moves of the piece in (x, y)
                    if [i, j] in possible_moves:

                        # If it is an enemy piece, allow move and eat the enemy piece
                        if not isinstance(unit, EmptyCell):
                            row_result.append({'type': 'piece', 'name': unit.__class__.__name__.lower(), 'colour': unit.colour, 'is_eaten': True})
                        
                        # If it is empty, allow move
                        else:
                            row_result.append({'type': 'move'})

                    # If the position is not in the possible moves of the piece in (x, y)
                    else:

                        # If it is another piece, leave them on the board
                        if not isinstance(unit, EmptyCell):
                            row_result.append({'type': 'piece', 'name': unit.__class__.__name__.lower(), 'colour': unit.colour})

                        # If it is an empty cell, do nothing
                        else:
                            row_result.append(None)

                # Append all the results of the above loop into 'result'
                result.append(row_result)

            # Brings result to the JQuery in UI
            eel.show_board(result)()

    # Check if piece can move to the destination by checking if the selected position is in the clean moves of the piece
    def can_move(self, x_from, y_from, x_to, y_to):
        return [x_to, y_to] in self.positions[x_from][y_from].get_clean_moves(self._board_simulation, x_from, y_from)
 
    # Removes a piece from position (x, y), or basically sets that position to an empty cell
    def remove(self, x, y):
        self.positions[x][y] = EmptyCell()

    # Places the piece in position (x, y)
    def place(self, unit, x, y):
        self.positions[x][y] = unit

    # Moves the piece
    def move(self, x_from, y_from, x_to, y_to):
        self.place(self.positions[x_from][y_from], x_to, y_to)
        self.remove(x_from, y_from)

    # Check if the player's king piece is checked by an enemy piece
    def is_checked(self, player_colour):
        result = False
        for x, row in enumerate(self.positions):
            for y, unit in enumerate(row):
                if isinstance(unit, King) and unit.colour == player_colour:
                    result = unit.is_targetted(self, x, y)
                
        return result
    
    # Check if the player can move (any) piece
    def has_clean_moves(self, player_colour):
        result = False

        # Loops through every piece that belongs to that player and checked if it has clean moves
        for x, row in enumerate(self.positions):
            for y, unit in enumerate(row):
                if not isinstance(unit, EmptyCell) and len(unit.get_clean_moves(self._board_simulation, x, y)) != 0 and unit.colour == player_colour:
                    result = True

        return result

# This class is responsible for the simulation of the board, incredibly crucial for the checked state
class BoardSimulation:
    def __init__(self, size):
        self.size = size
        self._board_state = BoardState(self)

    # Gets the current state of the board
    def get_current_state(self):
        copied_board = BoardState(self)

        # Copies everything in the current board state
        for x, row in enumerate(self._board_state.positions):
            for y, unit in enumerate(row):
                copied_board.place(unit, x, y)

        return copied_board

    # Saves the simulation of the board into the state of the board to be displayed in the UI
    def save_state(self, state):
        init_board = True

        # Checks every position in the board to see if it is empty
        for row in self._board_state.positions:
            for unit in row:
                if not isinstance(unit, EmptyCell):
                    init_board = False
        
        # Occurs if board is not empty
        if not init_board:
            for x, row in enumerate(state.positions):
                for y, unit in enumerate(row):

                    # If the unit is not in its original position, unit is 'moved'
                    if not isinstance(unit, EmptyCell) and type(unit) != type(self._board_state.positions[x][y]):
                        unit.moved()
        self._board_state = state