from .gamepiece import GamePiece

class King(GamePiece):
    def __init__(self, board, colour):
        self.symbol = 'K'
        super().__init__(board, colour)

    def get_possible_moves(self, x, y):
        unfiltered_result = []

        a = x
        b = y

        top = [a, b+1]
        top_right = [a+1, b+1]
        top_left = [a-1, b+1]
        bottom = [a, b-1]
        bottom_right = [a+1, b-1]
        bottom_left = [a-1, b-1]

        unfiltered_result.append(top)
        unfiltered_result.append(top_right)
        unfiltered_result.append(top_left)
        unfiltered_result.append(bottom)
        unfiltered_result.append(bottom_right)
        unfiltered_result.append(bottom_left)
            
        result = filter(lambda coord: self._board.check_bounds(coord[0], coord[1]), unfiltered_result)

        return [x for x in result]