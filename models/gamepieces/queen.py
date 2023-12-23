from .gamepiece import GamePiece

class Queen(GamePiece):
    symbol = 'Q'

    # Movement set of queen
    def get_possible_moves(self, board_state, x, y):
        result = []
        
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x + index, y]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x - index, y]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x, y + index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x, y - index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x + index, y + index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x - index, y + index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x + index, y - index]))
        result.extend(self.traverse(board_state, x, y, lambda x, y, index: [x - index, y - index]))

        return result
    