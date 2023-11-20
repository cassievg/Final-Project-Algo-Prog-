from string import ascii_uppercase

from models.exceptions import ChessException

class EmptyCell:
    def __init__(self):
        self.symbol = ' '
        self.colour = ' '


class Board:
    def __init__(self, size):
        self.size = size
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
        files = ascii_uppercase[0: self.size[0]]

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
            possible_moves = self.positions[x][y].get_possible_moves(x, y)

            files = ascii_uppercase[0: self.size[0]]

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
        return [x_to, y_to] in self.positions[x_from][y_from].get_possible_moves(x_from, y_from)
 
    def remove(self, x, y):
        self.positions[x][y] = EmptyCell()

    def place(self, unit, x, y):
        self.positions[x][y] = unit

    def move(self, x_from, y_from, x_to, y_to):
        if not self.can_move(x_from, y_from, x_to, y_to):
            raise ChessException('Movement illegal')
        
        self.place(self.positions[x_from][y_from], x_to, y_to)
        self.remove(x_from, y_from)

    def is_notation(self, notation):
        return notation[0] in ascii_uppercase and notation[1:].isnumeric()

    def notation_to_index(self, notation):
        index = [int(self.size[1]) - int(notation[1:]), ascii_uppercase.index(notation[0])]
        return index

    def index_to_notation(self, index):
        notation = str(ascii_uppercase[int(index[1])]) + str(int(self.size[1]) + 1 - int(index[0]))
        return notation

if __name__ == '__main__':
    board = Board([12, 13])
    print(board.notation_to_index('A10'))
    print(board.index_to_notation([4,0]))
