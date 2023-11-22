from libs.notation import get_files

from .exceptions import ChessException
from .gamepieces.king import King

class EmptyCell:
    def __init__(self):
        self.symbol = ' '
        self.colour = ' '


class BoardState:
    def __init__(self, board_simulation):
        self._board_simulation = board_simulation
        self.size = board_simulation.size
        self.positions = [
            [
                EmptyCell()
                for y in range(self.size[1])
            ]
            for x in range(self.size[0])
        ]
    
    def check_bounds(self, x, y):
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]:
            return False
        else:
            return True
        
    def is_empty(self, x, y):
        return isinstance(self.positions[x][y], EmptyCell)

    def is_empty_or_out_of_bounds(self, x, y):
        return not self.check_bounds(x, y) or self.is_empty(x, y)
    
    def show(self):
        files = get_files(self.size[1])

        files_row = '  '
        for file in files:
            files_row += file + '  '

        print(files_row)

        for index, unit_list in enumerate(self.positions):
            print(str(self.size[1] - index) + '|' + '|'.join([unit.colour + unit.symbol for unit in unit_list]) + '|')

    def show_possible_moves(self, x, y):
        if not self.check_bounds(x, y):
            raise ChessException('This is not in the board.')
        elif isinstance(self.positions[x][y], EmptyCell):
            raise ChessException('This is an empty cell.')
        else:
            possible_moves = self.positions[x][y].get_clean_moves(self._board_simulation, x, y)

            files = get_files(self.size[1])

            files_row = '  '
            for file in files:
                files_row += file + '  '

            print(files_row)
            for i, unit_list in enumerate(self.positions):
                row_string = ''
                for j, unit in enumerate(unit_list):
                    if [i, j] in possible_moves:
                        if not isinstance(unit, EmptyCell):
                            row_string += unit.colour + unit.symbol.lower()
                        else:
                            row_string += 'XX'
                    else:
                        row_string += unit.colour + unit.symbol

                    if j != len(unit_list) - 1:
                        row_string += '|'
                
                print(str(self.size[1] - i) + '|' + row_string + '|')

    def can_move(self, x_from, y_from, x_to, y_to):
        return [x_to, y_to] in self.positions[x_from][y_from].get_clean_moves(self._board_simulation, x_from, y_from)
 
    def remove(self, x, y):
        self.positions[x][y] = EmptyCell()

    def place(self, unit, x, y):
        self.positions[x][y] = unit

    def move(self, x_from, y_from, x_to, y_to):
        self.place(self.positions[x_from][y_from], x_to, y_to)
        self.remove(x_from, y_from)

    def is_checked(self, player_colour):
        result = False
        for x, row in enumerate(self.positions):
            for y, unit in enumerate(row):
                if isinstance(unit, King) and unit.colour == player_colour:
                    result = unit.is_targetted(self, x, y)
                
        return result
    
    def has_clean_moves(self, player_colour):
        result = False
        for x, row in enumerate(self.positions):
            for y, unit in enumerate(row):
                if not isinstance(unit, EmptyCell) and len(unit.get_clean_moves(self._board_simulation, x, y)) != 0 and unit.colour == player_colour:
                    result = True

        return result

class BoardSimulation:
    def __init__(self, size):
        self.size = size
        self._board_state = BoardState(self)

    def get_current_state(self):
        copied_board = BoardState(self)
        for x, row in enumerate(self._board_state.positions):
            for y, unit in enumerate(row):
                copied_board.place(unit, x, y)

        return copied_board

    def save_state(self, state):
        # Before replacing state, check if the gamepiece is moved by comparing current state with new one
        self._board_state = state
