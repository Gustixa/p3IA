import random
import time

def is_valid_move(board, player, row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if board[row][col] != 0:
        return False

    opponent = -player

    for direction in directions:
        dr, dc = direction
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            r += dr
            c += dc
            found_opponent = True

        if found_opponent and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            return True

    return False

def valid_moves(board, player):
    moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, player, row, col):
                moves.append((row, col))
    return moves

def apply_move(board, player, row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    board[row][col] = player
    opponent = -player

    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for rr, cc in pieces_to_flip:
                board[rr][cc] = player

def initial_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3] = board[4][4] = -1  # Blancas
    board[3][4] = board[4][3] = 1   # Negras
    return board

def initial_moves(turn):
    moves = [(2, 3), (2, 2), (3, 2)]
    if turn < len(moves):
        return moves[turn]
    return None

def simple_heuristic(board, player):
    moves = valid_moves(board, player)
    best_move = None
    max_pieces = -1
    for move in moves:
        row, col = move
        temp_board = [r[:] for r in board]
        apply_move(temp_board, player, row, col)
        pieces = sum([r.count(player) for r in temp_board])
        if pieces > max_pieces:
            max_pieces = pieces
            best_move = move
    return best_move

def minimax(board, player, depth, alpha, beta, maximizing):
    if depth == 0 or not valid_moves(board, player):
        return evaluate_board(board, player)
    
    if maximizing:
        max_eval = float('-inf')
        for move in valid_moves(board, player):
            row, col = move
            temp_board = [r[:] for r in board]
            apply_move(temp_board, player, row, col)
            eval = minimax(temp_board, -player, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves(board, player):
            row, col = move
            temp_board = [r[:] for r in board]
            apply_move(temp_board, player, row, col)
            eval = minimax(temp_board, -player, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

def evaluate_board(board, player):
    # Custom heuristic evaluation function
    score = 0
    opponent = -player
    # Weights for different positions on the board
    weights = [
        [100, -10, 10, 5, 5, 10, -10, 100],
        [-10, -20, 1, 1, 1, 1, -20, -10],
        [10, 1, 5, 2, 2, 5, 1, 10],
        [5, 1, 2, 1, 1, 2, 1, 5],
        [5, 1, 2, 1, 1, 2, 1, 5],
        [10, 1, 5, 2, 2, 5, 1, 10],
        [-10, -20, 1, 1, 1, 1, -20, -10],
        [100, -10, 10, 5, 5, 10, -10, 100]
    ]
    for row in range(8):
        for col in range(8):
            if board[row][col] == player:
                score += weights[row][col]
            elif board[row][col] == opponent:
                score -= weights[row][col]
    return score

def AI_MOVE(board, player):
    start_time = time.time()
    if len(valid_moves(board, player)) >= 54:  # Check if less than 10 moves played
        move = initial_moves(len(valid_moves(board, player)))
        if move:
            return move
    elif len(valid_moves(board, player)) < 54:  # Check if less than 54 moves played
        move = simple_heuristic(board, player)
        if move:
            return move
    else:
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in valid_moves(board, player):
            row, col = move
            temp_board = [r[:] for r in board]
            apply_move(temp_board, player, row, col)
            move_value = minimax(temp_board, -player, 4, alpha, beta, False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
            alpha = max(alpha, move_value)
        move = best_move

    if move is None:
        _valid_moves = valid_moves(board, player)
        move = random.choice(_valid_moves)

    end_time = time.time()
    if end_time - start_time > 3:
        raise Exception("Move took too long")

    return move
