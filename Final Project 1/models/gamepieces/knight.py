from .gamepiece import GamePiece

class Knight(GamePiece):
    symbol = 'N'

    def get_possible_moves(self, board_state, x, y):
        unfiltered_result = []

        a = x
        b = y
        top_right = [a+1, b+2]
        top_left = [a-1, b+2]
        right_top = [a+2, b+1]
        right_bottom = [a+2, b-1]
        bottom_right = [a+1, b-2]
        bottom_left = [a-1, b-2]
        left_top = [a-2, b+1]
        left_bottom = [a-2, b-1]

        unfiltered_result.append(top_right)
        unfiltered_result.append(top_left)
        unfiltered_result.append(right_top)
        unfiltered_result.append(right_bottom)
        unfiltered_result.append(bottom_right)
        unfiltered_result.append(bottom_left)
        unfiltered_result.append(left_top)
        unfiltered_result.append(left_bottom)

        result = filter(lambda coord: board_state.check_bounds(coord[0], coord[1]) and board_state.positions[coord[0]][coord[1]].colour != self.colour, unfiltered_result)

        return [x for x in result]