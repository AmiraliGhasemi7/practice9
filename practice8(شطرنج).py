import random

class Player:
    def __init__(self, name="Player", color="White"):
        self.name = name
        self.color = color
    
    def move(self):
        print(self.name, "(", self.color, ") is ready to move...")

class Bot:
    def __init__(self, name="Bot", color="Black"):
        self.name = name
        self.color = color
    
    def move(self):
        print(self.name, "(", self.color, ") is calculating move...")

class Piece:
    def __init__(self, color):
        self.color = color
    
    def valid_moves(self, position, board):
        raise NotImplementedError

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False  

    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves

class Queen(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False  

    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class Bishop(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class Horse(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves

class Pawn(Piece):
    def valid_moves(self, position, board):
        moves = []
        row, col = position
        direction = -1 if self.color == "White" else 1
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            start_row = 6 if self.color == "White" else 1
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
        if col - 1 >= 0 and 0 <= row + direction < 8:
            target = board[row + direction][col - 1]
            if target is not None and target.color != self.color:
                moves.append((row + direction, col - 1))
        if col + 1 < 8 and 0 <= row + direction < 8:
            target = board[row + direction][col + 1]
            if target is not None and target.color != self.color:
                moves.append((row + direction, col + 1))
        return moves

class Board:
    def __init__(self):
        self.board = self.create_board()
    
    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        board[0][0] = Rook('Black')
        board[0][1] = Horse('Black')
        board[0][2] = Bishop('Black')
        board[0][3] = Queen('Black')
        board[0][4] = King('Black')
        board[0][5] = Bishop('Black')
        board[0][6] = Horse('Black')
        board[0][7] = Rook('Black')
        for i in range(8):
            board[1][i] = Pawn('Black')
            board[6][i] = Pawn('White')
        board[7][0] = Rook('White')
        board[7][1] = Horse('White')
        board[7][2] = Bishop('White')
        board[7][3] = Queen('White')
        board[7][4] = King('White')
        board[7][5] = Bishop('White')
        board[7][6] = Horse('White')
        board[7][7] = Rook('White')
        return board
    
    def print_board(self):
        print("  a b c d e f g h")
        for i, row in enumerate(self.board):
            print(8 - i, end=" ")
            for piece in row:
                if piece is None:
                    print('.', end=' ')
                else:
                    letter = type(piece).__name__[0]
                    if letter == 'H':
                        letter = 'N'
                    if piece.color == 'Black':
                        letter = letter.lower()
                    print(letter, end=' ')
            print(8 - i)
        print("  a b c d e f g h")

    def move_piece(self, start_pos, end_pos):
        sr, sc = start_pos
        er, ec = end_pos
        piece = self.board[sr][sc]
        if piece is None:
            print("هیچ مهره‌ای در موقعیت شروع وجود ندارد!")
            return False
        valid_moves = piece.valid_moves((sr, sc), self.board)
        if (er, ec) not in valid_moves:
            print("حرکت انتخاب شده معتبر نیست!")
            return False
        self.board[er][ec] = piece
        self.board[sr][sc] = None
        if hasattr(piece, 'has_moved'):
            piece.has_moved = True
        return True

def parse_position(pos_str):
    columns = 'abcdefgh'
    col = columns.index(pos_str[0])
    row = 8 - int(pos_str[1])
    return (row, col)

def find_all_valid_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece is not None and piece.color == color:
                valid = piece.valid_moves((r, c), board)
                for vm in valid:
                    moves.append(((r, c), vm))
    return moves

player = Player()
bot = Bot()

game = Board()
game.print_board()

current_turn = "White"

while True:
    if current_turn == player.color:
        move_input = input("حرکت خود را وارد کن (مثال: e2 e4) یا exit برای خروج: ").strip()
        if move_input.lower() == 'exit':
            print("بازی تمام شد.")
            break
        try:
            start_str, end_str = move_input.split()
            start_pos = parse_position(start_str)
            end_pos = parse_position(end_str)
            if game.move_piece(start_pos, end_pos):
                game.print_board()
                current_turn = bot.color
            else:
                print("حرکت انجام نشد.")
        except Exception as e:
            print("خطای ورودی:", e)
    else:
        bot.move()
        valid_moves = find_all_valid_moves(game.board, bot.color)
        if not valid_moves:
            print("ربات هیچ حرکت معتبری ندارد، بازی تمام شد.")
            break
        move = random.choice(valid_moves)
        start_pos, end_pos = move
        game.move_piece(start_pos, end_pos)
        print(f"ربات حرکت کرد: {chr(start_pos[1]+97)}{8-start_pos[0]} -> {chr(end_pos[1]+97)}{8-end_pos[0]}")
        game.print_board()
        current_turn = player.color