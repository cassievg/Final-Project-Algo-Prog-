from libs.notation import notation_to_index, is_notation, index_to_notation

from models.exceptions import ChessException

class Player:
    def __init__(self, colour):
        self.colour = colour

    def get_select_piece(self, board_simulation, current_board_state):
        selected_piece = input('Select Piece (by chess notation): ')
        if not is_notation(selected_piece):
            raise ChessException('Invalid notation')

        selected_piece_index = notation_to_index(selected_piece, board_simulation.size[1])
        if not current_board_state.check_bounds(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is out of bounds')

        if current_board_state.is_empty(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is an empty cell')

        if self.colour != current_board_state.positions[selected_piece_index[0]][selected_piece_index[1]].colour:
            raise ChessException('This is an enemy piece')
        
        if len(current_board_state.positions[selected_piece_index[0]][selected_piece_index[1]].get_clean_moves(board_simulation, selected_piece_index[0], selected_piece_index[1])) == 0:
            raise ChessException('No possible moves')

        return selected_piece_index

    def get_move_piece(self, board, x_from, y_from):
        move_to = input('Move Piece (by chess notation): ')
        if move_to == '':
            return None

        if not is_notation(move_to):
            raise ChessException('Invalid notation')

        move_to_index = notation_to_index(move_to, board.size[1])
        if not board.can_move(x_from, y_from, move_to_index[0], move_to_index[1]):
            raise ChessException('Invalid move')
        
        return move_to_index
    
    def get_replace_piece(self, board, piece_coord, available_pieces):
        piece_notation = index_to_notation(piece_coord, board.size[1])
        symbols = {
            piece.symbol: piece
            for piece in available_pieces
        }
        change_to = input('Change %s to (%s): ' % (piece_notation, ', '.join(symbols)))

        if change_to not in symbols:
            raise ChessException('Invalid selection')
        
        change_to = symbols[change_to]

        return change_to