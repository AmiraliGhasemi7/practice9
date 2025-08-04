import random

board = [0] * 24

board[0] = 2
board[11] = 5
board[16] = 3
board[18] = 5

board[23] = -2
board[12] = -5
board[7] = -3
board[5] = -5

def print_board(board):
    print("صفحه بازی تخته نرد:")
    for i in range(12):
        print(str(i+1) + ": " + str(board[i]), end=' | ')
    print()
    for i in range(12, 24):
        print(str(i+1) + ": " + str(board[i]), end=' | ')
    print("\n")

def roll_one_die():
    return random.randint(1, 6)

def move_piece(board, player, start_pos, steps):
    if player == 1:
        new_pos = start_pos + steps
        if new_pos > 23:
            return False
    else:
        new_pos = start_pos - steps
        if new_pos < 0:
            return False
    if board[new_pos] * player >= -1:
        board[start_pos] -= player
        board[new_pos] += player
        return True
    else:
        return False

def player_turn(board):
    print_board(board)
    print("نوبت شماست")
    dice1 = roll_one_die()
    dice2 = roll_one_die()
    print("تاس‌ها: " + str(dice1) + " و " + str(dice2))
    moves = [dice1, dice2]
    for move in moves:
        valid_move = False
        while not valid_move:
            try:
                start_pos = int(input("خانه شروع حرکت برای مهره (۱ تا ۲۴) برای حرکت " + str(move) + ": ")) - 1
            except:
                print("لطفا یک عدد معتبر وارد کن.")
                continue
            if start_pos < 0 or start_pos > 23:
                print("عدد خانه باید بین 1 تا 24 باشد.")
                continue
            if board[start_pos] <= 0:
                print("خانه انتخاب شده مهره شما را ندارد.")
                continue
            valid_move = move_piece(board, 1, start_pos, move)

def bot_turn(board):
    print_board(board)
    print("نوبت ربات است")
    dice1 = roll_one_die()
    dice2 = roll_one_die()
    print("تاس‌ها: " + str(dice1) + " و " + str(dice2))
    moves = [dice1, dice2]
    for move in moves:
        possible_starts = []
        for i in range(24):
            if board[i] < 0:
                if move_piece(board[:], -1, i, move):
                    possible_starts.append(i)
        moved = False
        while not moved and len(possible_starts) > 0:
            start_pos = random.choice(possible_starts)
            if move_piece(board, -1, start_pos, move):
                print("ربات مهره از خانه " + str(start_pos + 1) + " حرکت داد به خانه " + str(start_pos + 1 + (-move if -1 == -1 else move)))
                moved = True
            else:
                possible_starts.remove(start_pos)
        if not moved:
            print("ربات نتوانست حرکت کند برای حرکت " + str(move))

def main():
    while True:
        player_turn(board)
        bot_turn(board)

if __name__ == "__main__":
    main()



