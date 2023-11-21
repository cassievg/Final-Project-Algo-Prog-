class GamePiece(object):
    def __init__(self, colour):
        self.colour = colour

    def is_targetted(self, current_board_state, x, y):
        result = False
        for enemy_x, row in enumerate(current_board_state.positions):
            for enemy_y, unit in enumerate(row):
                if not current_board_state.is_empty(enemy_x, enemy_y) and unit.colour != self.colour and [x, y] in unit.get_possible_moves(current_board_state, enemy_x, enemy_y):
                    result = True
        return result

    def get_possible_moves(self, current_board_state, x, y):
        return []

    def get_clean_moves(self, board_simulation, x, y):
        result = []
        current_board_state = board_simulation.get_current_state()
        for move in self.get_possible_moves(current_board_state, x, y):
            simulated_state = board_simulation.get_current_state()
            simulated_state.move(x, y, move[0], move[1])

            if not simulated_state.is_checked(self.colour):
                result.append(move)

        return result

    def traverse(self, current_board_state, x, y, calc_coord):
        output = []
        collision = False
        out_of_bounds = False
        index = 1
        while not collision and not out_of_bounds:
            possible_coord = calc_coord(x, y, index)
            if not current_board_state.check_bounds(possible_coord[0], possible_coord[1]):
                out_of_bounds = True
            else:
                if not current_board_state.is_empty(possible_coord[0], possible_coord[1]):
                    collision = True
                    if self.colour != current_board_state.positions[possible_coord[0]][possible_coord[1]].colour:
                        output.append(possible_coord)
                else:
                    output.append(possible_coord)
            index += 1

        return output