"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 19, 2026
"""

def is_empty(board): 
    #Checks if board is empty 
    for i in range (len(board)): 
        for j in range (len(board[0])): 
            if board[i][j] != " ": 
                return False 
    return True 
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    
    open_end = False 
    open_start = False 
    y_start = 0 
    x_start = 0 
    
    # End point
    if (0 <= x_end + d_x < len(board[0]) and 0 <= y_end + d_y < len(board)):
        if board[y_end + d_y][x_end + d_x] == " ":
            open_end = True
        
    #Start point 
    y_start = y_end - (length - 1) * d_y
    x_start = x_end - (length - 1) * d_x

    # Before the starting point
    if (0 <= x_start - d_x < len(board[0]) and 0 <= y_start - d_y < len(board)):
        if board[y_start - d_y][x_start - d_x] == " ":
            open_start = True


    #check bound type 
    if open_end == True and open_start == True: 
        return "OPEN" 
    if open_end == True or open_start == True: 
        return "SEMIOPEN" 
    else: 
        return "CLOSED"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x): 
    is_sequence = False 
    bounded = ""
    semi_open_seq_count = 0
    open_seq_count, semi_open_seq_count = 0, 0 

    x, y = x_start, y_start

    height = len(board)
    width = len(board[0])

    # Continue while a sequence of the given length fits on the board.
    while (0 <= y + (length - 1) * d_y < height and
           0 <= x + (length - 1) * d_x < width):
        is_sequence = True 
        for j in range (length): 
            if board[y + d_y * j][x + d_x * j] != col:
                is_sequence = False 
        #Before we check bounds, ensure there are no same-colored stones on either side of the sequence, so that the sequence is exactly the length given 
        #Check if the stone after the sequence is the same color 
        y_after = y + length * d_y
        x_after = x + length * d_x

        if 0 <= y_after < height and 0 <= x_after < width:
            if board[y_after][x_after] == col:
                is_sequence = False

        #Check if the stone before the sequence is the same color 
        y_before = y - d_y
        x_before = x - d_x

        if 0 <= y_before < height and 0 <= x_before < width:
            if board[y_before][x_before] == col:
                is_sequence = False

        
        #If the sequence is of given length, check bound and add to counter 
        if is_sequence == True:  
            y_end = y + (length - 1) * d_y
            x_end = x + (length - 1) * d_x

            bounded = is_bounded(board, y_end, x_end, length, d_y, d_x)

            if bounded == "OPEN": 
                open_seq_count += 1 
            if bounded == "SEMIOPEN": 
                semi_open_seq_count += 1 

        y += d_y
        x += d_x
    
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0

    height = len(board)
    width = len(board[0])

    d_y = 0
    d_x = 1
    x_start = 0
    # Horizontal: start from the leftmost column.
    for y_start in range(height):
        
        open_count, semi_open_count = detect_row(
            board, col, y_start, x_start, length, d_y, d_x
        )
        open_seq_count += open_count
        semi_open_seq_count += semi_open_count

    y_start = 0
    # Vertical and both diagonals: start from the top row.
    for d_x in [0, 1, -1]:
        d_y = 1  # Direction for vertical and diagonal searches.
        for x_start in range(width):
            open_count, semi_open_count = detect_row(
                board, col, y_start, x_start, length, d_y, d_x
            )
            open_seq_count += open_count
            semi_open_seq_count += semi_open_count

    d_y = 1
    # Remaining diagonals: start from the left or right edge.
    for d_x in [1, -1]:
        if d_x == 1:
            x_start = 0
        else:
            x_start = width - 1
        # Start from the second row to avoid double counting the top-left and top-right corners.
        for y_start in range(1, height):
            open_count, semi_open_count = detect_row(
                board, col, y_start, x_start, length, d_y, d_x
            )
            open_seq_count += open_count
            semi_open_seq_count += semi_open_count

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    max_score = -float("inf") # Ensures first available move will always be selected, regarless of negaive 
    curr_score = 0 
    move_y = 0
    move_x = 0 

    #Iterates through whole board and finds a blank spot 
    for j in range (len(board)):  
        for i in range (len(board[0])): 
            if board[j][i] == " ": 
                #Puts a hypothetical black stone 
                board [j][i] = "b" 
                #Calclates score with that black stone 
                curr_score = score(board)
                #If the score is larger than the maximum score, set that score to the new maximum score 
                if curr_score > max_score: 
                    max_score = curr_score 
                    #Save the position of the black stone that gives the max score 
                    move_x = i 
                    move_y = j 
                #Remove the hypothetical black stone from the board 
                board [j][i] = " "
    return move_y, move_x


def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
    
def is_win(board):
    empty_count = 0 

    for i in range (len(board)): 
        for j in range (len(board)): 
            #Ensures referenced point is not empty 
            if board[i][j]!= " ": 
                #Horizontal 
                count = 0 
                #Only check the next 4 postitions right if available 
                if j < len(board) - 4: 
                    #Check next 4 positions right 
                    for k in range(5): 
                        if board [i][j+k] == board[i][j]: 
                            count += 1 
                        else: 
                            count = 0  
                    #If a positiion exists after the 5th group 
                    if j + 5 < len(board): 
                    #If the stone after the group of 5 is also the same color, no win 
                        if board[i][j+5] == board[i][j]: 
                            count = 0 

                    #If a positiion exists before the 5th group 
                    if j - 1 >= 0: 
                    #If the stone before the group of 5 is also the same color, no win 
                        if board[i][j-1] == board[i][j]: 
                            count = 0 

                    #If 5 in a row are the same stone, we have a winner 
                    if count == 5: 
                        if board[i][j] == "b": 
                            return ("Black won") 
                        else: 
                            return ("White won")
                #Vertical 
                #Only check the next 4 postition down if available 
                count = 0 
                if i < len(board) - 4: 
                    for k in range(5): 
                        if board [i+k][j] == board[i][j]: 
                            count += 1 
                        else: 
                            count = 0  
                    #If a positiion exists after the 5th group 
                    if i + 5 < len(board): 
                    #If the stone after the group of 5 is also the same color, no win 
                        if board[i+5][j] == board[i][j]: 
                            count = 0 

                    #If a positiion exists before the 5th group 
                        if i - 1 >= 0: 
                        #If the stone before the group of 5 is also the same color, no win 
                            if board[i-1][j] == board[i][j]: 
                                count = 0 

                    #If 5 in a row are the same stone, we have a winner 
                    if count == 5: 
                        if board[i][j] == "b": 
                            return ("Black won") 
                        else: 
                            return ("White won")
                
                
                #Diagonal top-left to bottom-right 
                #Only check the next 4 postition both right and down if available 
                count = 0 
                if i < len(board) - 4 and j < len(board) - 4: 
                    for k in range(5): 
                        if board [i+k][j+k] == board[i][j]: 
                            count += 1 
                        else: 
                            count = 0  

                    #If a positiion exists after the 5th group 
                    if j + 5 < len(board) and i + 5 < len(board): 
                    #If the stone after the group of 5 is also the same color, no win 
                        if board[i+5][j+5] == board[i][j]: 
                            count = 0 
                    
                    #If a positiion exists before the 5th group 
                    if j - 1 >= 0 and i - 1 >= 0:  
                    #If the stone before the group of 5 is also the same color, no win 
                        if board[i-1][j-1] == board[i][j]: 
                            count = 0 
                            
                    #If 5 in a row are the same stone, we have a winner 
                    if count == 5: 
                        if board[i][j] == "b": 
                            return ("Black won") 
                        else: 
                            return ("White won")
                
                #Diagonal top-right to bottom-left 
                #Only check the next 4 postition both left and down if available 
                count = 0 
                if i < len(board) - 4 and j >= 4: 
                    for k in range(5): 
                        if board [i+k][j-k] == board[i][j]: 
                            count += 1 
                        else: 
                            count = 0  

                    #If a positiion exists after the 5th group 
                    if j - 5 >= 0 and i + 5 < len(board): 
                    #If the stone after the group of 5 is also the same color, no win 
                        if board[i+5][j-5] == board[i][j]: 
                            count = 0 

                    #If a positiion exists before the 5th group 
                    if j + 1 < len(board) and i - 1 >= 0: 
                    #If the stone before the group of 5 is also the same color, no win 
                        if board[i-1][j+1] == board[i][j]: 
                            count = 0 

                    #If 5 in a row are the same stone, we have a winner 
                    if count == 5: 
                        if board[i][j] == "b": 
                            return ("Black won") 
                        else: 
                            return ("White won")
            else: 
                #If position is empty 
                empty_count += 1 
    
    if empty_count == 0: 
        #No empty positions on the board. Board is full and nobody won.  
        return ("Draw") 
    else: 
        #Nobody won but there are still empty positions available 
        return ("Continue playing")
    

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

if __name__ == '__main__':
    print (play_gomoku(8)) 
    
