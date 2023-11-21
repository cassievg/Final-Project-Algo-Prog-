from .gamepiece import GamePiece

class Bishop(GamePiece):
    symbol = 'B'

    def get_possible_moves(self, board_state, x, y):
        result = []

        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x + index, y + index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x - index, y + index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x + index, y - index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x - index, y - index]))

        return result
