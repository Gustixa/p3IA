import random

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
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, player, row, col):
                valid_moves.append((row, col))
    return valid_moves

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
    return sum([r.count(player) for r in board])

def AI_MOVE(board, player):
    if len(board[board == 0]) >= 54:  # Check if less than 10 moves played
        move = initial_moves(len(board[board != 0]))
        if move:
            return move
    elif len(board[board != 0]) < 54:  # Check if less than 54 moves played
        return simple_heuristic(board, player)
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
        return best_move

    # Fallback to random move if no other move found (shouldn't happen)
    _valid_moves = valid_moves(board, player)
    return random.choice(_valid_moves)