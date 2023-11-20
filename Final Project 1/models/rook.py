from .gamepiece import GamePiece

class Rook(GamePiece):
    def __init__(self, board, colour):
        self.symbol = 'R'
        super().__init__(board, colour)

    def get_possible_moves(self, x, y):
        result = []
        
        result.extend(self.traverse(x, y, lambda x, y, index: [x + index, y]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x - index, y]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x, y + index]))
        result.extend(self.traverse(x, y, lambda x, y, index: [x, y - index]))

        return result
    

if __name__ == '__main__':
    rook = Rook()
    print(rook.get_possible_moves(1, 6))
    print(rook.get_possible_moves(0, 0))
    print(rook.get_possible_moves(4, 7))
