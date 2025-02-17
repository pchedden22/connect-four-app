import random
import math

class ConnectFour:
    def __init__(self, rows=6, columns=7, win_length=4):
        self.rows = rows
        self.columns = columns
        self.win_length = win_length
        self.board = [['' for _ in range(columns)] for _ in range(rows)]
        self.current_player = 'player1'
        self.winner = None
        self.tie = False

    def drop_piece(self, column):
        if self.winner or self.tie:
            return False

        for row in range(self.rows - 1, -1, -1):
            if not self.board[row][column]:
                self.board[row][column] = self.current_player
                if self.check_winner(row, column):
                    self.winner = self.current_player
                elif all(self.board[0][col] for col in range(self.columns)):
                    self.tie = True
                self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
                return True
        return False

    def check_winner(self, row, column):
        def count_consecutive(row, col, d_row, d_col):
            piece = self.board[row][col]
            count = 0
            while 0 <= row < self.rows and 0 <= col < self.columns and self.board[row][col] == piece:
                count += 1
                row += d_row
                col += d_col
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for d_row, d_col in directions:
            if count_consecutive(row, column, d_row, d_col) + count_consecutive(row, column, -d_row, -d_col) - 1 >= self.win_length:
                return True
        return False
    
    def check_horizontal(self, row, winLength, opponent):
        #opponent = 'player2' if self.current_player == 'player1' else 'player1'
        for col in range(self.columns - winLength + 1):
            count = 0
            empty_spot = None
            for i in range(winLength):
                if self.board[row][col + i] == opponent:
                    count += 1
                elif self.board[row][col + i] == '':
                    if empty_spot is None:
                        empty_spot = col + i
                    else:
                        empty_spot = None
                        break
                else:
                    break
            if count == winLength - 1 and empty_spot is not None:
                return empty_spot
        return None

    
    def check_vertical(self, winLength, playerCheck):
        #opponent = 'player2' if self.current_player == 'player1' else 'player1'
        for col in range(self.columns):
            for row in range(self.rows - winLength + 1):
                count = 0
                empty_spot = None
                for i in range(winLength):
                    if self.board[row + i][col] == playerCheck:
                        count += 1
                    elif self.board[row + i][col] == '':
                        if empty_spot is None:
                            empty_spot = col
                        else:
                            empty_spot = None
                            break
                    else:
                        break
                if count == winLength - 1 and empty_spot is not None:
                    return empty_spot
        return None


    
    def check_diagonal(self, winLength, playerCheck):
        #opponent = 'player2' if self.current_player == 'player1' else 'player1'
        # Check positive slope diagonals
        for col in range(self.columns - winLength + 1):
            for row in range(self.rows - winLength + 1):
                count = 0
                empty_spot = None
                for i in range(winLength):
                    if self.board[row + i][col + i] == playerCheck:
                        count += 1
                    elif self.board[row + i][col + i] == '':
                        if empty_spot is None:
                            empty_spot = col + i
                        else:
                            empty_spot = None
                            break
                    else:
                        break
                if count == winLength - 1 and empty_spot is not None:
                    return empty_spot

        # Check negative slope diagonals
        for col in range(self.columns - winLength + 1):
            for row in range(winLength - 1, self.rows):
                count = 0
                empty_spot = None
                for i in range(winLength):
                    if self.board[row - i][col + i] == playerCheck:
                        count += 1
                    elif self.board[row - i][col + i] == '':
                        if empty_spot is None:
                            empty_spot = col + i
                        else:
                            empty_spot = None
                            break
                    else:
                        break
                if count == winLength - 1 and empty_spot is not None:
                    return empty_spot

        return None


        



    ######################################################
    #   Checks if middle columns have a placable spot.   #
    #   Parameters: None                                 #
    #   Returns: Int, or None                            #
    ######################################################
    def check_middle(self):

        # Create a set of available columns.
        colSet = set()

        # Checks if middle columns have a placable spot.
        for col in range((self.columns // 2) - 1, (self.columns // 2) + 2):
            for row in range(self.rows):
                if self.board[row][col] == '':
                    colSet.add(col)
                    break  # Stops checking the column if a placable spot is found.

        # If placable spots are found, return a random column from the set.
        if colSet:
            colList = list(colSet)
            return random.choice(colList)
        
        # Return None if no placable spot is found.
        return None

    def winPossCheck(self, winLength, playerCheck):
        
        for row in range(self.rows):
            if self.check_horizontal(row, winLength, playerCheck) is not None:
                print("Possible route! Horizontal!")
                return self.check_horizontal(row, winLength, playerCheck)
            elif self.check_vertical(winLength, playerCheck) is not None:
                print("Possible route! Vertical!")
                return self.check_vertical(winLength, playerCheck)
            elif self.check_diagonal(winLength, playerCheck) is not None:
                print("Possible route! Diagonal!")
                return self.check_diagonal(winLength, playerCheck)

        return None

    def oppSetupWinCheck(self, player, col):
        if col is not None:
            winMove = self.winPossCheck(self.win_length - 1,player)
            if winMove is not None:
                return winMove
        return None



    def find_winning_move(self, player):
        for row in range(self.rows):
            if self.check_horizontal(row, self.win_length, player) is not None:
                return self.check_horizontal(row, self.win_length, player)
        for col in range(self.columns):
            if self.check_vertical(self.win_length, player) is not None:
                
                return self.check_vertical(self.win_length, player)
        if self.check_diagonal(self.win_length, player) is not None:
            return self.check_diagonal(self.win_length, player)
        return None


    def ai_move(self):
        available_columns = [col for col in range(self.columns) if not self.board[0][col]]
        if available_columns:
            return random.choice(available_columns)
        return None
    
    ##################################################################
    #   AI MOVES: MEDIUM                                             #
    #   70% chance to block, usually places in middle if no block.   #
    #   Params: None                                                 #
    #   Returns: Int, or None                                        #
    ##################################################################
    def ai_move_medium(self):
        print('ai_move_medium')
        block_probability = 0.70  # 70% chance to block the opponent
        middle_probability = 0.7  # 70% chance to move in the middle
        blocking_move = self.find_winning_move('player1')
        
        if blocking_move is not None and random.random() < block_probability:
            print('Block!')
            return blocking_move
        
        elif blocking_move is None and random.random() < middle_probability:
            print('Middle!')
            return self.check_middle()


        # Otherwise, make a random move
        print('No block! Making random move...')
        return self.ai_move()

    ##################################################################
    #   AI MOVES: HARD                                               #
    #   80% chance to block, usually places in middle if no block.   #
    #   Params: None                                                 #
    #   Returns: Int, or None                                        #
    ##################################################################
    def ai_move_hard(self):
        print('ai_move_hard')
        block_probability = 0.99  # 80% chance to block the opponent
        middle_probability = 0.7  # 70% chance to move in the middle

        blocking_move = self.find_winning_move('player1')
        winPossImmediate = self.winPossCheck(self.win_length, 'player2')
        winPossFuture = self.winPossCheck(self.win_length - 1, 'player2')
        oppSetupWin = self.oppSetupWinCheck('player1', winPossFuture)
        
        if winPossImmediate is not None:
            print('Immediate win!')
            return winPossImmediate

        elif blocking_move is not None and oppSetupWin is None and random.random() < block_probability:
            print('Block!')
            return blocking_move
        
        elif winPossFuture is not None and oppSetupWin is None:
            print('Future win!')
            return winPossFuture
        
        elif blocking_move is None and random.random() < middle_probability:
            print('Middle!')
            return self.check_middle()


        # Otherwise, make a random move
        print('No block! Making random move...')
        return self.ai_move()
    
    def ai_move_very_hard(self):
        best_score = -math.inf
        best_move = None
        depth = 4

        # First, check if there's a winning move available
        for col in range(self.columns):
            if self.board[0][col] == '':
                row = self.get_next_open_row(col)
                self.board[row][col] = 'player2'  # AI player
                if self.check_winner(row, col):
                    self.board[row][col] = ''
                    return col  # Immediately return the winning move
                self.board[row][col] = ''

        for col in range(self.columns):
            if self.board[0][col] == '':
                row = self.get_next_open_row(col)
                self.board[row][col] = 'player2'
                score = self.minimax(depth - 1, -math.inf, math.inf, False)
                self.board[row][col] = ''

                if score > best_score:
                    best_score = score
                    best_move = col

        return best_move


    ##################################################################
    #   Applies AI move depending on difficulty.                     #
    #   Params: String                                               #
    #   Returns: Int, or None                                        #
    ##################################################################
    def apply_ai_move(self, difficulty):
        if self.current_player == 'player2' and not self.winner and not self.tie:
            if difficulty == 'medium':
                ai_column = self.ai_move_medium()
            elif difficulty == 'hard':
                ai_column = self.ai_move_hard()
            elif difficulty == 'very_hard':
                ai_column = self.ai_move_very_hard()
            else:
                ai_column = self.ai_move()
            
            if ai_column is not None:
                #self.drop_piece(ai_column)
                return ai_column
        return None
    
    ##################################################################
    #   Places piece in column.                                      #
    #   Params: Int, String                                          #
    #   Returns: Int, or None                                        #
    ##################################################################
    def place_piece(self, column, player):
        for row in range(self.rows - 1, -1, -1):
            if not self.board[row][column]:
                self.board[row][column] = player
                return row
        return None

    ##################################################################
    #   Removes piece in column.                                     #
    #   Params: Int, Int                                             #
    #   Returns: No Return                                           #
    ##################################################################
    def remove_piece(self, row, column):
        self.board[row][column] = ''


    ##################################################################
    #   Finds next open row.                                         #
    #   Params: Int                                                  #
    #   Returns: Int or None                                         #
    ##################################################################
    
    def get_next_open_row(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == '':
                return row
        return None

    ################################################################################
    #   Determines score of AI in current board. Based on center column control.   #
    #   Params: Int, Int                                                           #
    #   Returns: No Return                                                         #
    ################################################################################
    def evaluate_board(self):
        score = 0

        # Center control
        score += self.score_center('player2')
        score -= self.score_center('player1')  # Opponent's center control

        # Score Horizontal
        for row in range(self.rows):
            for col in range(self.columns - 3):
                line = [self.board[row][col + i] for i in range(4)]
                score += self.score_line(line, 'player2')
                score -= self.score_line(line, 'player1')  # Opponent's potential

        # Score Vertical
        for col in range(self.columns):
            for row in range(self.rows - 3):
                line = [self.board[row + i][col] for i in range(4)]
                score += self.score_line(line, 'player2')
                score -= self.score_line(line, 'player1')  # Opponent's potential

        # Score positive diagonal
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                line = [self.board[row + i][col + i] for i in range(4)]
                score += self.score_line(line, 'player2')
                score -= self.score_line(line, 'player1')  # Opponent's potential

        # Score negative diagonal
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                line = [self.board[row - i][col + i] for i in range(4)]
                score += self.score_line(line, 'player2')
                score -= self.score_line(line, 'player1')  # Opponent's potential

        return score


    def score_center(self, player):
        score = 0
        center_column = self.columns // 2
        for row in range(self.rows):
            if self.board[row][center_column] == player:
                score += 3  # Adjust the weight as needed
        return score
    
    def score_line(self, line, player):
        score = 0
        opponent = 'player1' if player == 'player2' else 'player2'

        if line.count(player) == 4:
            score += 100  # Winning line
        elif line.count(player) == 3 and line.count('') == 1:
            score += 10  # Potential winning line
        elif line.count(player) == 2 and line.count('') == 2:
            score += 5   # Possible setup
        if line.count(opponent) == 3 and line.count('') == 1:
            score -= 80  # Block opponent's potential win
        
        return score




    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return self.evaluate_board()

        if maximizingPlayer:
            max_value = -math.inf
            for col in range(self.columns):
                if self.board[0][col] == '':
                    row = self.get_next_open_row(col)
                    self.board[row][col] = 'player2'  # AI player

                    # Check if this move wins the game
                    if self.check_winner(row, col):
                        self.board[row][col] = ''
                        return 100000  # Return a very high value for winning move

                    value = self.minimax(depth - 1, alpha, beta, False)
                    self.board[row][col] = ''
                    max_value = max(max_value, value)
                    alpha = max(alpha, max_value)
                    if beta <= alpha:
                        break
            return max_value
        else:
            min_value = math.inf
            for col in range(self.columns):
                if self.board[0][col] == '':
                    row = self.get_next_open_row(col)
                    self.board[row][col] = 'player1'  # Opponent player

                    # Check if this move wins the game
                    if self.check_winner(row, col):
                        self.board[row][col] = ''
                        return -100000  # Return a very low value to prioritize blocking

                    value = self.minimax(depth - 1, alpha, beta, True)
                    self.board[row][col] = ''
                    min_value = min(min_value, value)
                    beta = min(beta, min_value)
                    if beta <= alpha:
                        break
            return min_value



