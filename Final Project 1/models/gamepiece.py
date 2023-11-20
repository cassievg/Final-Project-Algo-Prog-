class GamePiece(object):
    def __init__(self, board, colour):
        self._board = board
        self.colour = colour

    def traverse(self, x, y, calc_coord):
        output = []
        collision = False
        out_of_bounds = False
        index = 1
        while not collision and not out_of_bounds:
            possible_coord = calc_coord(x, y, index)
            if not self._board.check_bounds(possible_coord[0], possible_coord[1]):
                out_of_bounds = True
            else:
                if not self._board.is_empty(possible_coord[0], possible_coord[1]):
                    collision = True
                    if self.colour != self._board.positions[possible_coord[0]][possible_coord[1]].colour:
                        output.append(possible_coord)
                else:
                    output.append(possible_coord)
            index += 1

        return output