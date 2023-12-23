from .gamepiece import GamePiece

class King(GamePiece):
    symbol = 'K'

    # Movement set of king
    def get_possible_moves(self, board_state, x, y):
        unfiltered_result = []

        a = x
        b = y

        top = [a, b+1]
        top_right = [a+1, b+1]
        top_left = [a-1, b+1]
        bottom = [a, b-1]
        bottom_right = [a+1, b-1]
        bottom_left = [a-1, b-1]
        left = [a+1, b]
        right = [a-1, b]

        unfiltered_result.append(top)
        unfiltered_result.append(top_right)
        unfiltered_result.append(top_left)
        unfiltered_result.append(bottom)
        unfiltered_result.append(bottom_right)
        unfiltered_result.append(bottom_left)
        unfiltered_result.append(right)
        unfiltered_result.append(left)

        # Remove appended results that are out of bounds
        result = filter(lambda coord: board_state.check_bounds(coord[0], coord[1]) and board_state.positions[coord[0]][coord[1]].colour != self.colour, unfiltered_result)

        return [x for x in result]
    
    def get_clean_moves(self, board_simulation, x, y):

        # Calls get_clean_moves from gamepiece
        result = super().get_clean_moves(board_simulation, x, y)

        # Gets current board state
        board_state = board_simulation.get_current_state()

        # The part below focuses on chess castling rules

        # If the king piece is not in check and has not moved
        if not self.is_targetted(board_state, x, y) and not self.has_moved:

            # Allow queenside castling
            queenside_castling = True
            castling_y_left = y - 1

            # Check on the left side of the king
            while castling_y_left > 0:
                
                # If there is a piece blocking the king or it is targetted by an enemy piece, disallow queenside castling
                if not board_state.is_empty(x, castling_y_left) or self.is_targetted(board_state, x, castling_y_left):
                    queenside_castling = False

                castling_y_left -= 1
            
            # Check if the castling rook is still present and has not moved, otherwise disallow queenside castling
            if not board_state.is_rook(x, castling_y_left) or (board_state.is_rook(x, castling_y_left) and board_state.positions[x][castling_y_left].has_moved):
                queenside_castling = False

            # Allow kingside castling
            kingside_castling = True
            castling_y_right = y + 1

            #Check on the right side of the king
            while castling_y_right < board_state.size[1] - 1:

                # If there is a piece blocking the king or it is targetted by an enemy piece, disallow kingside castling
                if not board_state.is_empty(x, castling_y_right) or self.is_targetted(board_state, x, castling_y_right):
                    kingside_castling = False

                castling_y_right += 1
            
            # Check if the castling rook is still present and has no moved, otherwise disallow kingside castling
            if not board_state.is_rook(x, castling_y_right) or (board_state.is_rook(x, castling_y_right) and board_state.positions[x][castling_y_right].has_moved):
                kingside_castling = False

            # Append both kingside and queenside castling to the possible moves of king if the castling requirements are met
            if queenside_castling:
                result.append([x, y-2])
                
            if kingside_castling:
                result.append([x, y+2])

        return result