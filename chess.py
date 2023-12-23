import eel

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
        self.is_running = True

    def _initialize_pieces(self):
        current_board_state = self._board_simulation.get_current_state()

        # Player 1 initial pieces
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

        # Player 2 initial pieces
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

        # Save the initial positions and pieces to the board state
        self._board_simulation.save_state(current_board_state)

    # Gets the position of pawn when it reaches the end of the board
    def get_pawn_at_border(self, current_board_state):
        result = None
        last_pawn_position = [0, self._board_simulation.size[1] - 1]
        x = last_pawn_position[self._no_of_turns % 2]

        # If there is a pawn at the end of the board, take its position (x, y)
        for y, unit in enumerate(current_board_state.positions[x]):
            if isinstance(unit, Pawn):
                result = [x, y]

        return result

    # To check if checkmate has happened
    def is_checkmate(self):
        current_player = self._players[self._no_of_turns % 2]
        current_board_state = self._board_simulation.get_current_state()

        # Returns true if the player's king piece is checked, and the player cannot move any piece
        return current_board_state.is_checked(current_player.colour) and not current_board_state.has_clean_moves(current_player.colour)
    
    # To check if stalemate has happened
    def is_stalemate(self):
        current_player = self._players[self._no_of_turns % 2]
        current_board_state = self._board_simulation.get_current_state()

        # Returns true if the current player cannot move, but the king is not necessarily in check
        return not current_board_state.has_clean_moves(current_player.colour)
    
    # This def is to control how each turn works
    def _next_turn(self):
        done = False
        error = ''

        # Loops until the turn is done or the game stops running
        while not done and self.is_running:
            try:

                # Takes current player and board state first
                current_player = self._players[self._no_of_turns % 2]
                current_board_state = self._board_simulation.get_current_state()

                # First check if the current player is checked. If yes, tell the player by displaying it in the UI
                if current_board_state.is_checked(current_player.colour):
                    eel.show_game_stats('Player %s Turn - You are checked' % current_player.name)
                else:
                    eel.show_game_stats('Player %s Turn - %s' % (current_player.name, error))

                # Shows the current board
                current_board_state.show()

                # Player selects a piece to move
                selected_position = current_player.get_select_piece(self, self._board_simulation, current_board_state)

                # The board will show the possible moves of the piece
                current_board_state.show_possible_moves(selected_position[0], selected_position[1])

                # Player selects the position to move the piece
                move_piece = current_player.get_move_piece(self, current_board_state, selected_position[0], selected_position[1])

                if move_piece is not None:

                    # Moves piece
                    current_board_state.move(selected_position[0], selected_position[1], move_piece[0], move_piece[1])

                    # Puts the state of the board BEFORE player moved, into a separate variable
                    prev_board_state = self._board_simulation.get_current_state()

                    # This series of conditions are to check for castling
                    # They check the king's position before and after the player moves
                    # Kings move differently during castling. After the king moves, the rook will automatically move to the castling position
                    if isinstance(prev_board_state.positions[7][4], King) and isinstance(current_board_state.positions[7][2], King):
                        current_board_state.move(7, 0, 7, 3)
                        
                    if isinstance(prev_board_state.positions[7][4], King) and isinstance(current_board_state.positions[7][6], King):
                        current_board_state.move(7, 7, 7, 5)

                    if isinstance(prev_board_state.positions[0][4], King) and isinstance(current_board_state.positions[0][2], King):
                        current_board_state.move(0, 0, 0, 3)
                        
                    if isinstance(prev_board_state.positions[0][4], King) and isinstance(current_board_state.positions[0][6], King):
                        current_board_state.move(0, 7, 0, 5)

                    # This is for when a pawn has reached the end of the board
                    border_pawn = self.get_pawn_at_border(current_board_state)

                    # If there is a pawn
                    if border_pawn is not None:

                        # Gives selection of pieces to convert that pawn, and replace the pawn
                        available_pieces = [Rook, Bishop, Knight, Queen]
                        chosen_piece = current_player.get_replace_piece(self, available_pieces)
                        current_board_state.place(chosen_piece(current_player.colour), border_pawn[0], border_pawn[1])
                    
                    # Saves the board simulation
                    self._board_simulation.save_state(current_board_state)

                    # Moves to next turn
                    self._no_of_turns += 1
                    done = True

            except ChessException as err:
                error = err

            except Exception as err:
                raise err
        
    # To stop the game
    def stop(self):
        self.is_running = False
    
    # To run the game
    def run(self):

        # Initial size of the board
        eel.init_board([8, 8])()

        # Place the pieces in initial position
        self._initialize_pieces()

        # Allow turns to keep cycling UNLESS checkmate or stalemate happens, or the game stopped
        while not self.is_checkmate() and not self.is_stalemate() and self.is_running:
            self._next_turn()

        # If checkmate happens and the game is still running
        if self.is_checkmate() and self.is_running:

            # Gets the winner and shows the aftermath
            self._no_of_turns += 1
            current_player = self._players[self._no_of_turns % 2]
            current_board_state = self._board_simulation.get_current_state()
            current_board_state.show()
            
            # This is for the JQuery in the UI
            # UI will tell who won
            eel.show_game_stats('Player %s won' % current_player.name)

        # If stalemate happens and the game is still running
        elif self.is_stalemate() and self.is_running:
            current_board_state = self._board_simulation.get_current_state()
            current_board_state.show()

            # UI will tell that the game ended with a draw
            eel.show_game_stats('Draw')

running_game = None
# Expose to UI JQuery
@eel.expose

# Starts the game
def start_game():

    # Global variable
    global running_game

    # For game restart, stops game and deletes the current states and saves
    if running_game:
        running_game.stop()
    del running_game

    # Prepares new game
    running_game = Game([Player('1', 'white'), Player('2', 'black')])
    running_game.run()


if __name__ == '__main__':
    eel.init('views')
    eel.start('index.html')