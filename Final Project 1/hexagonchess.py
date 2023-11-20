from models.board import Board

from models.player import Player

from models.pawn import Pawn
from models.king import King
from models.knight import Knight
from models.queen import Queen
from models.rook import Rook
from models.bishop import Bishop

from models.exceptions import ChessException

class Game:
    def __init__(self, players):
        self._players = players
        self._no_of_turns = 0
        self._board = Board([8, 8])

    def _initialize_pieces(self):
        # Player 1 Pieces
        self._board.place(Rook(self._board, self._players[0].colour), 7, 0)
        self._board.place(Knight(self._board, self._players[0].colour), 7, 1)
        self._board.place(Bishop(self._board, self._players[0].colour), 7, 2)
        self._board.place(Queen(self._board, self._players[0].colour), 7, 3)
        self._board.place(King(self._board, self._players[0].colour), 7, 4)
        self._board.place(Bishop(self._board, self._players[0].colour), 7, 5)
        self._board.place(Knight(self._board, self._players[0].colour), 7, 6)
        self._board.place(Rook(self._board, self._players[0].colour), 7, 7)

        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 0)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 1)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 2)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 3)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 4)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 5)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 6)
        self._board.place(Pawn(self._board, self._players[0].colour, 'up'), 6, 7)

        # Player 2 Pieces
        self._board.place(Rook(self._board, self._players[1].colour), 0, 0)
        self._board.place(Knight(self._board, self._players[1].colour), 0, 1)
        self._board.place(Bishop(self._board, self._players[1].colour), 0, 2)
        self._board.place(King(self._board, self._players[1].colour), 0, 3)
        self._board.place(Queen(self._board, self._players[1].colour), 0, 4)
        self._board.place(Bishop(self._board, self._players[1].colour), 0, 5)
        self._board.place(Knight(self._board, self._players[1].colour), 0, 6)
        self._board.place(Rook(self._board, self._players[1].colour), 0, 7)

        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 0)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 1)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 2)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 3)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 4)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 5)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 6)
        self._board.place(Pawn(self._board, self._players[1].colour, 'down'), 1, 7)

    def is_checkmate(self):
        return False
    
    def is_stalemate(self):
        return False
    
    def _next_turn(self):
        done = False
        while not done:
            try:
                current_player = self._players[self._no_of_turns % 2]
                print('Player %s Turn' % current_player.colour)
                print()

                self._board.show()
                print()

                selected_position = current_player.select_piece(self._board)
                print()

                self._board.show_possible_moves(selected_position[0], selected_position[1])

                move_piece = current_player.move_piece(self._board, selected_position[0], selected_position[1])
                print()

                if move_piece is not None:
                    self._board.move(selected_position[0], selected_position[1], move_piece[0], move_piece[1])
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

if __name__ == '__main__':
    game = Game([Player('W'), Player('B')])
    game.run()