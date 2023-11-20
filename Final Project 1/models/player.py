from models.exceptions import ChessException

class Player:
    def __init__(self, colour):
        self.colour = colour

    def select_piece(self, board):
        selected_piece = input('Select Piece (by chess notation): ')
        if not board.is_notation(selected_piece):
            raise ChessException('Invalid notation')

        selected_piece_index = board.notation_to_index(selected_piece)
        if not board.check_bounds(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is out of bounds')

        if board.is_empty(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is an empty cell')

        if self.colour != board.positions[selected_piece_index[0]][selected_piece_index[1]].colour:
            raise ChessException('This is an enemy piece')
        
        if len(board.positions[selected_piece_index[0]][selected_piece_index[1]].get_possible_moves(selected_piece_index[0], selected_piece_index[1])) == 0:
            raise ChessException('No possible moves')

        return selected_piece_index

    def move_piece(self, board, x_from, y_from):
        move_to = input('Move Piece (by chess notation): ')
        if move_to == '':
            return None

        if not board.is_notation(move_to):
            raise ChessException('Invalid notation')

        move_to_index = board.notation_to_index(move_to)
        if not board.can_move(x_from, y_from, move_to_index[0], move_to_index[1]):
            raise ChessException('Invalid move')
        
        return move_to_index
