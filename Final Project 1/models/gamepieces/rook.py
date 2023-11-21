from .gamepiece import GamePiece

class Rook(GamePiece):
    symbol = 'R'

    def get_possible_moves(self, board_state, x, y):
        result = []
        
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x + index, y]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x - index, y]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x, y + index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x, y - index]))

        return result
    