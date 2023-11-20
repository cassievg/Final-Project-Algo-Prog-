from .gamepiece import GamePiece

class Bishop(GamePiece):
    def __init__(self, board, colour):
        self.symbol = 'B'
        super().__init__(board, colour)

    def get_possible_moves(self, x, y):
        result = []

        result.extend(self.traverse(x, y, lambda x, y, index: [x + index, y + index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x - index, y + index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x + index, y - index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x - index, y - index]))

        return result


if __name__ == '__main__':
    bishop = Bishop('white')
    print(bishop.get_possible_moves(1, 6))