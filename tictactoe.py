def display_board(board):
    print("\n")
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print("\n")

def check_winner(board, player):

    winning_positions = [
        [0, 1, 2],[3, 4, 5],[6, 7, 8],[0, 3, 6],
        [1, 4, 7],[2, 5, 8],[0, 4, 8],[2, 4, 6]
    ]

    for position in winning_positions:
        if (board[position[0]] == player and
            board[position[1]] == player and
            board[position[2]] == player):
            return True

    return False

def play_game():

    board = [" "] * 9

    current_player = "X"

    print("\nWelcome to Tic-Tac-Toe!")
    print("Player 1: X")
    print("Player 2: O")

    while True:

        display_board(board)

        print(f"Player {current_player} 's turn")
        choice = input("Enter a position (1-9): ")

        if choice == "":
            print("Please enter a position!")
            continue

        if not choice.isdigit():
            print("Invalid input! Please enter a number.")
            continue

        position = int(choice)

        if position < 1 or position > 9:
            print("Invalid position! Choose between 1 and 9.")
            continue

        if board[position - 1] != " ":
            print("This position is already occupied. Try again!")
            continue

        board[position - 1] = current_player

        if check_winner(board, current_player):
            display_board(board)
            print("Congratulations! Player", current_player, "wins!")
            break

        if " " not in board:
            display_board(board)
            print("The game is a Draw!")
            break

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


while True:

    play_game()

    while True:
        answer = input("\nDo you want to play again? (yes/no): ").lower()

        if answer == "yes" or answer == "y":
            break
        elif answer == "no" or answer == "n":
            print("\nThank you for playing Tic-Tac-Toe!")
            exit()
        else:
            print("Please enter yes or no.")