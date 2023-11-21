from models.board import BoardSimulation

from models.player import Player

from models.gamepieces.pawn import Pawn
from models.gamepieces.king import King
from models.gamepieces.knight import Knight
from models.gamepieces.queen import Queen
from models.gamepieces.rook import Rook
from models.gamepieces.bishop import Bishop

from models.exceptions import ChessException

class Game:
    def __init__(self, players):
        self._players = players
        self._no_of_turns = 0
        self._board_simulation = BoardSimulation([8, 8])

    def _initialize_pieces(self):
        current_board_state = self._board_simulation.get_current_state()
        # Player 1 Pieces
        current_board_state.place(Rook(self._players[0].colour), 7, 0)
        current_board_state.place(Knight(self._players[0].colour), 7, 1)
        current_board_state.place(Bishop(self._players[0].colour), 7, 2)
        current_board_state.place(Queen(self._players[0].colour), 7, 3)
        current_board_state.place(King(self._players[0].colour), 7, 4)
        current_board_state.place(Bishop(self._players[0].colour), 7, 5)
        current_board_state.place(Knight(self._players[0].colour), 7, 6)
        current_board_state.place(Rook(self._players[0].colour), 7, 7)

        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 0)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 1)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 2)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 3)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 4)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 5)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 6)
        current_board_state.place(Pawn(self._players[0].colour, 'up'), 6, 7)

        # Player 2 Pieces
        current_board_state.place(Rook(self._players[1].colour), 0, 0)
        current_board_state.place(Knight(self._players[1].colour), 0, 1)
        current_board_state.place(Bishop(self._players[1].colour), 0, 2)
        current_board_state.place(Queen(self._players[1].colour), 0, 3)
        current_board_state.place(King(self._players[1].colour), 0, 4)
        current_board_state.place(Bishop(self._players[1].colour), 0, 5)
        current_board_state.place(Knight(self._players[1].colour), 0, 6)
        current_board_state.place(Rook(self._players[1].colour), 0, 7)

        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 0)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 1)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 2)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 3)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 4)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 5)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 6)
        current_board_state.place(Pawn(self._players[1].colour, 'down'), 1, 7)
        self._board_simulation.save_state(current_board_state)

    def is_checkmate(self):
        current_player = self._players[self._no_of_turns % 2]
        current_board_state = self._board_simulation.get_current_state()
        return current_board_state.is_checked(current_player.colour) and not current_board_state.has_clean_moves(current_player.colour)
    
    def is_stalemate(self):
        current_player = self._players[self._no_of_turns % 2]
        current_board_state = self._board_simulation.get_current_state()
        return current_board_state.has_clean_moves(current_player.colour)
    
    def _next_turn(self):
        done = False
        while not done:
            try:
                current_player = self._players[self._no_of_turns % 2]
                current_board_state = self._board_simulation.get_current_state()

                if current_board_state.is_checked(current_player.colour):
                    print('Player %s is checked' % current_player.colour)

                print('Player %s Turn' % current_player.colour)
                print()

                current_board_state.show()
                print()

                selected_position = current_player.select_piece(self._board_simulation, current_board_state)
                print()

                current_board_state.show_possible_moves(selected_position[0], selected_position[1])

                move_piece = current_player.move_piece(current_board_state, selected_position[0], selected_position[1])
                print()

                if move_piece is not None:
                    current_board_state.move(selected_position[0], selected_position[1], move_piece[0], move_piece[1])
                    self._board_simulation.save_state(current_board_state)
                    self._no_of_turns += 1
                    done = True
            except ChessException as err:
                print(err)
            except Exception as err:
                raise err

    def run(self):
        self._initialize_pieces()
        while not self.is_checkmate() and not self.is_stalemate():
            self._next_turn()

        if self.is_checkmate():
            self._no_of_turns += 1
            current_player = self._players[self._no_of_turns % 2]
            print('Player %s won' % current_player.colour)

        elif self.is_stalemate():
            print('Draw')

if __name__ == '__main__':
    game = Game([Player('W'), Player('B')])
    game.run()