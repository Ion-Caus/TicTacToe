import random
import math

class Board:
    def __init__(self):
        self.cells = [  '1', '2', '3',
                        '4', '5', '6',
                        '7', '8', '9',]

    # display the board  -  print()
    def __repr__(self):
        return f"""
                 __ __ __
                |{self.cells[0]} |{self.cells[1]} |{self.cells[2]} |
                |__|__|__|
                |{self.cells[3]} |{self.cells[4]} |{self.cells[5]} |
                |__|__|__|
                |{self.cells[6]} |{self.cells[7]} |{self.cells[8]} |
                |__|__|__|
                """

    def updateCell(self, pos, symbol):
        self.cells[pos] = symbol

    def isValid(self, pos):
        if self.cells[pos] in ' 123456789':
            return True
        return False

    def isWinner(self, symbol):
        return (# checks rows
                (self.cells[0] == symbol and self.cells[1] == symbol and self.cells[2] == symbol )  or 
                (self.cells[3] == symbol and self.cells[4] == symbol and self.cells[5] == symbol )  or 
                (self.cells[6] == symbol and self.cells[7] == symbol and self.cells[8] == symbol )  or
                # checks columns 
                (self.cells[0] == symbol and self.cells[3] == symbol and self.cells[6] == symbol )  or 
                (self.cells[1] == symbol and self.cells[4] == symbol and self.cells[7] == symbol )  or 
                (self.cells[2] == symbol and self.cells[5] == symbol and self.cells[8] == symbol )  or 
                # checks diagonals
                (self.cells[0] == symbol and self.cells[4] == symbol and self.cells[8] == symbol )  or 
                (self.cells[2] == symbol and self.cells[4] == symbol and self.cells[6] == symbol ))

    def isFull(self):
        for i in range(9):
            if self.cells[i] in ' 123456789':
                return False
        return True 

    def clearBoard(self):
        self.__init__()

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

        if self.symbol == 'O':
            self.symbol = '\x1b[31mO\x1b[0m'    # 'O' red
            self.opponent = '\x1b[32mX\x1b[0m'   # 'X' green
        else:
            self.symbol = '\x1b[32mX\x1b[0m' # 'X' green
            self.opponent = '\x1b[31mO\x1b[0m'   # 'O' red

    def move(self, board):
        # get input
        while True:
            try:
                pos = int(input('Pos (1-9): ')) - 1
                if pos < 0 or pos > 8:
                    raise ValueError
            except ValueError:
                print('Invalid input. Try again')
            else:
                # if no error then break
                break

        # place the symbol
        if board.isValid(pos):
            board.updateCell(pos, self.symbol)
        else:
            print(f'Try another pos. The pos {pos + 1} is unavailable')
            self.move(board)

    def bestMove(self, board):
        bestScore = -math.inf
        bestMove = None

        for i in range(9):
            if board.isValid(i):
                board.updateCell(i, self.symbol)
                score = self.minmax(board, 0, False)
                board.updateCell(i, str(i + 1)) #place back the number

                if score > bestScore:
                    bestScore = score 
                    bestMove = i
        board.updateCell(bestMove, self.symbol)

    def minmax(self, board, depth, isMaximizer, alpha = -math.inf, beta = math.inf):
        if board.isWinner(self.opponent):
            return -10 + depth
        elif board.isWinner(self.symbol):
            return 10 - depth
        elif board.isFull():
            return 0 

        if isMaximizer:
            bestScore = -math.inf
            for i in range(9):
                if board.isValid(i):
                    board.updateCell(i, self.symbol)
                    score = self.minmax(board, depth+1, False, alpha, beta) + random.randint(-5,5)
                    board.updateCell(i, str(i + 1)) #place back the number
                    bestScore = max(score, bestScore)

                    # alpha beta pruning
                    alpha = max(alpha, bestScore)
                    if alpha >= beta:
                        break

            return bestScore
        else:
            bestScore = math.inf
            for i in range(9):
                if board.isValid(i):
                    board.updateCell(i, self.opponent)
                    score = self.minmax(board, depth+1, True, alpha, beta) + random.randint(-5,5)
                    board.updateCell(i, str(i + 1)) #place back the number
                    bestScore = min(score, bestScore)

                    # alpha beta pruning
                    beta = min(beta, bestScore)
                    if alpha >= beta:
                        break

            return bestScore


if __name__ == "__main__":
    import os

    GameBoard = Board()

    Me = Player('X')
    AI = Player('O')

    os.system('clear')
    print(GameBoard)

    while True:

        Me.move(GameBoard)

        os.system('clear')
        print(GameBoard)


        if GameBoard.isWinner(Me.symbol):
            print('Im the winner!!\n')
            break
        elif GameBoard.isFull():
            print('Its a tie\n')
            break

        AI.bestMove(GameBoard)
        
        os.system('clear')
        print(GameBoard)

        if GameBoard.isWinner(AI.symbol):
            print('AI is the winner!!\n')
            break
