from .gamepiece import GamePiece

class Queen(GamePiece):
    def __init__(self, board, colour):
        self.symbol = 'Q'
        super().__init__(board, colour)

    def get_possible_moves(self, x, y):
        result = []
        
        result.extend(self.traverse(x, y, lambda x, y, index: [x + index, y]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x - index, y]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x, y + index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x, y - index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x + index, y + index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x - index, y + index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x + index, y - index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x - index, y - index]))

        return result
    

if __name__ == '__main__':
    queen = Queen()
    print(queen.get_possible_moves(1, 6))