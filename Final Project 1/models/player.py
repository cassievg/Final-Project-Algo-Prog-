import eel
from libs.notation import index_to_notation

from models.exceptions import ChessException


class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def _input_selected_position(self, game):
        result = eel.get_selected_position()()
        while result is None:
            eel.sleep(0.1)
            if not game.is_running:
                raise ChessException('Stop')
            result = eel.get_selected_position()()
        return result
    
    def _input_replace_pawn(self, game):
        eel.show_replace_pawn()()
        result = eel.get_replace_pawn()()
        while result is None:
            eel.sleep(0.1)
            if not game.is_running:
                raise ChessException('Stop')
            result = eel.get_replace_pawn()()
        return result

    def get_select_piece(self, game, board_simulation, current_board_state):
        selected_piece_index = self._input_selected_position(game)

        if not current_board_state.check_bounds(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is out of bounds')

        if current_board_state.is_empty(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is an empty cell')

        if self.colour != current_board_state.positions[selected_piece_index[0]][selected_piece_index[1]].colour:
            raise ChessException('This is an enemy piece')
        
        if len(current_board_state.positions[selected_piece_index[0]][selected_piece_index[1]].get_clean_moves(board_simulation, selected_piece_index[0], selected_piece_index[1])) == 0:
            raise ChessException('No possible moves')

        return selected_piece_index

    def get_move_piece(self, game, board, x_from, y_from):        
        move_to_index = self._input_selected_position(game)

        if not board.can_move(x_from, y_from, move_to_index[0], move_to_index[1]):
            raise ChessException('Invalid move')
        
        return move_to_index
    
    def get_replace_piece(self, game, available_pieces):
        symbols = {
            piece.symbol: piece
            for piece in available_pieces
        }
        change_to = self._input_replace_pawn(game)

        if change_to not in symbols:
            raise ChessException('Invalid selection')
        
        change_to = symbols[change_to]

        return change_to