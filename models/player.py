import eel
from libs.notation import index_to_notation

from models.exceptions import ChessException

class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    # Takes the selected position from UI using eel (for moving)
    def _input_selected_position(self, game):

        # Puts the selected position in result
        result = eel.get_selected_position()()

        # If user does not input, keep looping but with a 0.1 second delay to prevent lag and crashing
        while result is None:
            eel.sleep(0.1)

            # If the game stops running, raise error
            if not game.is_running:
                raise ChessException('Stop')
            
            result = eel.get_selected_position()()

        return result
    
    # Takes the selected piece to replace pawn (after it has reached the end of the board)
    def _input_replace_pawn(self, game):

        # JQuery in UI runs this
        eel.show_replace_pawn()()

        # Puts the selected piece in result
        result = eel.get_replace_pawn()()

        # If user does not input, keep looping but with a 0.1 second delay to prevent lag and crashing
        while result is None:
            eel.sleep(0.1)

            # If the game stops running, raise error
            if not game.is_running:
                raise ChessException('Stop')
            
            result = eel.get_replace_pawn()()

        return result

    # Gets the piece the current player selects
    def get_select_piece(self, game, board_simulation, current_board_state):
        selected_piece_index = self._input_selected_position(game)

        # Raise error if player selects something out of the board
        if not current_board_state.check_bounds(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is out of bounds')

        # Raise error if player selects an empty cell
        if current_board_state.is_empty(selected_piece_index[0], selected_piece_index[1]):
            raise ChessException('This is an empty cell')

        # Raise error if player selects an enemy piece
        if self.colour != current_board_state.positions[selected_piece_index[0]][selected_piece_index[1]].colour:
            raise ChessException('This is an enemy piece')
        
        # Raise error if player selects a piece that cannot move
        if len(current_board_state.positions[selected_piece_index[0]][selected_piece_index[1]].get_clean_moves(board_simulation, selected_piece_index[0], selected_piece_index[1])) == 0:
            raise ChessException('No possible moves')

        return selected_piece_index

    # Gets the piece move
    def get_move_piece(self, game, board, x_from, y_from):        
        move_to_index = self._input_selected_position(game)

        # If piece cannot move, raise error
        if not board.can_move(x_from, y_from, move_to_index[0], move_to_index[1]):
            raise ChessException('Invalid move')
        
        return move_to_index
    
    # Gets the piece to replace the pawn at the end of the board
    def get_replace_piece(self, game, available_pieces):
        symbols = {
            piece.symbol: piece
            for piece in available_pieces
        }

        change_to = self._input_replace_pawn(game)

        # If the piece selected is an invalid piece, raise error
        if change_to not in symbols:
            raise ChessException('Invalid selection')
        
        # Changes the pawn to the selected piece
        change_to = symbols[change_to]

        return change_to