import chess
from chessboard import display
import time

class GameState:
    def __init__(self, board=None, is_white_turn=True):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
        self.is_white_turn = is_white_turn  # True = White's turn, False = Black's turn

    def check_goal(self):
        # Check if the game is over
        if self.board.is_checkmate():
            return not self.is_white_turn  # The opponent just made a winning move
        return None

    def is_over(self):
        return self.board.is_game_over()

    def generate_moves(self):
        # Generate next possible states
        next_states = []
        for move in self.board.legal_moves:
            temp_board = self.board.copy()
            temp_board.push(move)
            next_states.append(GameState(temp_board, not self.is_white_turn))
        return next_states

    def __str__(self):
        return str(self.board)

    def __eq__(self, other):
        return self.board.fen() == other.board.fen() and self.is_white_turn == other.is_white_turn

    def __hash__(self):
        return hash((self.board.fen(), self.is_white_turn))

    def evaluate_position(self):
        """
        Evaluation function for chess positions.

        - Positive = good for White.
        - Negative = good for Black.
        """

        # Step 1: End of game conditions
        if self.board.is_checkmate():
            return -1000 if self.board.turn == chess.WHITE else 1000
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
            return 0

        # Step 2a: Material balance
        evaluation_score = 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        for square, piece in self.board.piece_map().items():
            piece_value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                evaluation_score += piece_value
            else:
                evaluation_score -= piece_value

        # Step 2b: Center control
        central_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        for square in central_squares:
            piece = self.board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    evaluation_score += 0.2
                else:
                    evaluation_score -= 0.2

        # Step 2c: Mobility
        temp_board = self.board.copy()
        temp_board.turn = chess.WHITE
        white_moves_count = len(list(temp_board.legal_moves))
        temp_board.turn = chess.BLACK
        black_moves_count = len(list(temp_board.legal_moves))
        evaluation_score += 0.05 * (white_moves_count - black_moves_count)

        # Step 2d: King safety
        white_king_square = self.board.king(chess.WHITE)
        black_king_square = self.board.king(chess.BLACK)

        if white_king_square:
            attackers = self.board.attackers(chess.BLACK, white_king_square)
            if attackers:
                evaluation_score -= 0.5 * len(attackers)

        if black_king_square:
            attackers = self.board.attackers(chess.WHITE, black_king_square)
            if attackers:
                evaluation_score += 0.5 * len(attackers)

        return evaluation_score


# ---------------- Minimax with Alpha-Beta ----------------
def minimax(state, depth, alpha, beta, is_maximizing, max_depth):
    if state.is_over() or depth == max_depth:
        return state.evaluate_position(), None

    best_move = None

    if is_maximizing:  # White
        max_score = float('-inf')
        for child in state.generate_moves():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, False, max_depth)

            if eval_score > max_score:
                max_score = eval_score
                best_move = child.board.peek()

            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break

        return max_score, best_move

    else:  # Black
        min_score = float('inf')
        for child in state.generate_moves():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, True, max_depth)

            if eval_score < min_score:
                min_score = eval_score
                best_move = child.board.peek()

            beta = min(beta, eval_score)
            if alpha >= beta:
                break

        return min_score, best_move


# ---------------- Gameplay ----------------
def play_chess():
    game_state = GameState(is_white_turn=True)  # White starts
    search_depth = 3  # Adjust for difficulty
    gui_board = display.start()  # GUI board

    print("Artificial Intelligence – Assignment 3")
    print("Chess AI with Minimax + Alpha-Beta")
    print("You are playing as White (UCI format, e.g., e2e4)")

    while not game_state.is_over():
        # Update GUI
        display.update(game_state.board.fen(), gui_board)

        # Quit check
        if display.check_for_quit():
            break

        if game_state.is_white_turn:  # Human
            try:
                move_input = input("Enter move (e.g., e2e4, g1f3, a7a8q) or 'quit': ")

                if move_input.lower() == 'quit':
                    break

                move = chess.Move.from_uci(move_input)
                if move in game_state.board.legal_moves:
                    new_board = game_state.board.copy()
                    new_board.push(move)
                    game_state = GameState(new_board, False)
                else:
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Invalid input! Use UCI format (e.g., e2e4).")
                continue

        else:  # AI move
            print("AI is thinking...")
            start_time = time.time()
            eval_score, best_move = minimax(game_state, 0, float('-inf'), float('inf'), False, search_depth)
            end_time = time.time()

            print(f"AI thought for {end_time - start_time:.2f} seconds")

            if best_move:
                new_board = game_state.board.copy()
                new_board.push(best_move)
                game_state = GameState(new_board, True)
                print(f"AI plays: {best_move.uci()}")
            else:
                # Fallback move
                legal_moves = list(game_state.board.legal_moves)
                if legal_moves:
                    move = legal_moves[0]
                    new_board = game_state.board.copy()
                    new_board.push(move)
                    game_state = GameState(new_board, True)
                    print(f"AI plays (fallback): {move.uci()}")
                else:
                    break

    # Game finished
    print("\nGame Over!")
    display.update(game_state.board.fen(), gui_board)

    if game_state.board.is_checkmate():
        print("Checkmate! " + ("White" if not game_state.is_white_turn else "Black") + " wins!")
    elif game_state.board.is_stalemate():
        print("Stalemate! Draw.")
    elif game_state.board.is_insufficient_material():
        print("Draw due to insufficient material.")
    elif game_state.board.can_claim_draw():
        print("Draw by repetition or 50-move rule.")

    time.sleep(3)
    display.terminate()


if __name__ == "__main__":
    play_chess()
