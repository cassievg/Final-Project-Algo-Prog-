from .gamepiece import GamePiece

class Pawn(GamePiece):
    def __init__(self, board, colour, direction):
        self.symbol = 'P'
        self.direction = direction
        super().__init__(board, colour)

    def get_possible_moves(self, x, y):
        unfiltered_result = []
        if self.direction == 'up' and self._board.is_empty_or_out_of_bounds(x-1, y):
            unfiltered_result.append([x-1, y])
        elif self.direction == 'down' and self._board.is_empty_or_out_of_bounds(x+1, y):
            unfiltered_result.append([x+1, y])

        if self.direction == 'up' and x == 6 and self._board.is_empty_or_out_of_bounds(x-1, y) and self._board.is_empty_or_out_of_bounds(x-2, y):
            unfiltered_result.append([x-2, y])
        elif self.direction == 'down' and x == 1 and self._board.is_empty_or_out_of_bounds(x+1, y) and self._board.is_empty_or_out_of_bounds(x+2, y):
            unfiltered_result.append([x+2, y])

        if self.direction == 'up':
            if not self._board.is_empty_or_out_of_bounds(x-1, y-1) and self.colour != self._board.positions[x-1][y-1].colour:
                unfiltered_result.append([x-1, y-1])
            if not self._board.is_empty_or_out_of_bounds(x-1, y+1) and self.colour != self._board.positions[x-1][y+1].colour:
                unfiltered_result.append([x-1, y+1])
        if self.direction == 'down':
            if not self._board.is_empty_or_out_of_bounds(x+1, y+1) and self.colour != self._board.positions[x+1][y+1].colour:
                unfiltered_result.append([x+1, y+1])
            if not self._board.is_empty_or_out_of_bounds(x+1, y-1) and self.colour != self._board.positions[x+1][y-1].colour:
                unfiltered_result.append([x+1, y-1])

        result = filter(lambda coord: self._board.check_bounds(coord[0], coord[1]), unfiltered_result)

        return [x for x in result]