from .gamepiece import GamePiece

class Pawn(GamePiece):
    symbol = 'P'
    
    def __init__(self, colour, direction):

        # Direction matters when it comes to pawns
        self.direction = direction
        super().__init__(colour)

    # Movement sets of pawns for each player 1 and player 2
    def get_possible_moves(self, board_state, x, y):
        unfiltered_result = []

        # Pawns can move by one cell
        if self.direction == 'up' and board_state.is_empty_or_out_of_bounds(x-1, y):
            unfiltered_result.append([x-1, y])
        elif self.direction == 'down' and board_state.is_empty_or_out_of_bounds(x+1, y):
            unfiltered_result.append([x+1, y])

        # Pawns can also move by two cells, but only if it is at the player's half of the board
        if self.direction == 'up' and x == 6 and board_state.is_empty_or_out_of_bounds(x-1, y) and board_state.is_empty_or_out_of_bounds(x-2, y):
            unfiltered_result.append([x-2, y])
        elif self.direction == 'down' and x == 1 and board_state.is_empty_or_out_of_bounds(x+1, y) and board_state.is_empty_or_out_of_bounds(x+2, y):
            unfiltered_result.append([x+2, y])

        # Pawns can move diagonally to eat enemy piece only if there is one
        if self.direction == 'up':
            if not board_state.is_empty_or_out_of_bounds(x-1, y-1) and self.colour != board_state.positions[x-1][y-1].colour:
                unfiltered_result.append([x-1, y-1])
            if not board_state.is_empty_or_out_of_bounds(x-1, y+1) and self.colour != board_state.positions[x-1][y+1].colour:
                unfiltered_result.append([x-1, y+1])
        if self.direction == 'down':
            if not board_state.is_empty_or_out_of_bounds(x+1, y+1) and self.colour != board_state.positions[x+1][y+1].colour:
                unfiltered_result.append([x+1, y+1])
            if not board_state.is_empty_or_out_of_bounds(x+1, y-1) and self.colour != board_state.positions[x+1][y-1].colour:
                unfiltered_result.append([x+1, y-1])

        # Remove appended results that are out of bounds
        result = filter(lambda coord: board_state.check_bounds(coord[0], coord[1]), unfiltered_result)

        return [x for x in result]