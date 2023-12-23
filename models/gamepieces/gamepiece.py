class GamePiece(object):
    def __init__(self, colour):
        self.colour = colour

        # This one is very important for castling, as chess castling has rules for it to be done
        self.has_moved = False

    # When the piece moves, make has_moved true
    def moved(self):
        self.has_moved = True

    # Check if piece is targetted by an enemy piece (or if it is in the enemy piece's possible moves)
    def is_targetted(self, current_board_state, x, y):
        result = False
        for enemy_x, row in enumerate(current_board_state.positions):
            for enemy_y, unit in enumerate(row):
                if not current_board_state.is_empty(enemy_x, enemy_y) and unit.colour != self.colour and [x, y] in unit.get_possible_moves(current_board_state, enemy_x, enemy_y):
                    result = True
        return result

    # Get possible moves of the selected piece
    def get_possible_moves(self, current_board_state, x, y):
        return []

    # If king is checked, only a few pieces can move, and those moves must be able to remove the checked state of the player
    def get_clean_moves(self, board_simulation, x, y):
        result = []
        current_board_state = board_simulation.get_current_state()

        # Loops through every single possible moves of the piece in (x, y)
        for move in self.get_possible_moves(current_board_state, x, y):
            simulated_state = board_simulation.get_current_state()
            simulated_state.move(x, y, move[0], move[1])

            # If that move stops the checked state, append to result
            if not simulated_state.is_checked(self.colour):
                result.append(move)

        return result

    # An easier method, basically, for the pieces that can move from one end of the board to the other
    def traverse(self, current_board_state, x, y, calc_coord):
        output = []
        collision = False
        out_of_bounds = False
        index = 1

        # While there isn't any other piece blocking the selected piece and while it is inside of the board, put the position in the output
        while not collision and not out_of_bounds:
            possible_coord = calc_coord(x, y, index)

            # If the possible coordinate is outside of the board, set out of bounds to true
            if not current_board_state.check_bounds(possible_coord[0], possible_coord[1]):
                out_of_bounds = True

            else:

                # If the possible coordinate is not empty (it has a piece)
                if not current_board_state.is_empty(possible_coord[0], possible_coord[1]):
                    collision = True

                    # If the possible coordinate is not empty but it is blocked by enemy piece, allow move to this coordinate
                    if self.colour != current_board_state.positions[possible_coord[0]][possible_coord[1]].colour:
                        output.append(possible_coord)
                else:
                    output.append(possible_coord)
            index += 1

        return output