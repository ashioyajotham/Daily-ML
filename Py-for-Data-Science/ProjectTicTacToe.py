
from random import randrange

def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console
    for i in range (0, len(board), 3):
        print("+-----"*3 + "+")
        print("|     "*3 + "|")
        print("|  " + str(board[i]) + \
                 "  | "  + str(board[i + 1]) + \
                "  |  "  + str(board[i +2]) +  " | ")

def enter_move(board):
    #The function accepts the board current status, asks the user about their move
    #checks the input and updates the board according to the user's decision
    freeFields = make_list_of_free_fields(board)
    pos = int(input("Enter your move: "))

    while(pos < 1 or pos > 9):
        print("Please enter number between 1 and 9")
        pos = int(input("Enter your move: "))

    while True:
        if pos in freeFields:
            board[pos - 1] = "0"
            break
        else:
            print("Position already filled")
            pos = int(input("Enter your move: "))
    display_board(board)

def make_list_of_free_fields (board):
    #The function browses the board and builds a list of all the free squares
    # the list consists of tuples, while each is a pair of
    freeFields = []
    for i in range (len(board)):
        if board[i] != '0' and board[i] != 'X':
            freeFields.append(board[i])
    #print(freeFields)
    return freeFields

def victory_for(board, sign):
    #The function analyses the board status in order to check if
    # the player using 'O's or 'X's has won the game
    arrangements = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], 
                   [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for i in range(len(arrangements)):
        pos1, pos2, pos3 = arrangements[i][0] - 1, arrangements[i][0] - 1, \
                        arrangements[i][2] - 1
        if (str(board[pos1]) == sign) and (str (board[pos2]) == sign) \
            and (str (board[pos3]) == sign):
            return True


def draw_move(board):
    #The function draws the computer's move and updates the board
    freeFields = make_list_of_free_fields(board)
    pos = randrange(1, 10)
    while True:
        if pos in freeFields:
            board[pos - 1] = 'X'
            break
        else:
            pos = randrange(1, 10)
    display_board(board)

    #main program
    #board: 3 * 3squares
    board = [1, 2, 3, 4, 'X', 6, 7, 8, 9]

    display_board(board)
    while True:
        #check if all board is filled
        moves = 0
        for i in range (len(board)):
            if board[i] == '0' or board[i] == 'X':
                moves += 1
        if moves == len(board):
            print('Game is Tie')
            break

        # user turn
        enter_move()
        if victory_for(board, 0):
            print('you won')
            break
        #computer turn
        draw_move(board)
        if victory_for(board, "X"):
            print("Computer won !!!")
            break