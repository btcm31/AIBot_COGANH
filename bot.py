import random
import copy
from board import Board

class Bot:
    def __init__(self,timeExceed):
        self.timeExceed = timeExceed
        self.preState = []
    def __minimax_alpha_beta(self, board:Board, depth, alpha, beta, player,isOptimizer,dt):
        temp = Board(board.state)
        if depth == 0 or board.is_end(player):
            return None, board.evaluate(-player)
        best_move = None
        Eval = -9999 if isOptimizer else 9999
        for move in board.getAllAvailableMoves(player,dt):
            new_board = copy.deepcopy(board.make_move(move[0], move[1],player))
            m = board.checkBAY(board,new_board)
            currEval = self.__minimax_alpha_beta(new_board, depth - 1, alpha, beta,-player,not isOptimizer,m)[1]
            if isOptimizer and Eval < currEval:
                Eval = currEval
                best_move = move
                alpha = max(alpha, Eval)
                if beta <= alpha:
                    break
            elif not isOptimizer and Eval > currEval:
                Eval = currEval
                best_move = move
                beta = min(beta, Eval)
                if beta <= alpha:
                    break
        return best_move, Eval
    def move(self, board:Board, player):
        dt = [[0,0],[0,0]]
        if self.preState==[]:
            m = Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]])
            dt = board.checkBAY(Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]]),board)
        else:
            dt = board.checkBAY(Board(self.preState),board)
        if dt[0]!=dt[1]:
            result = self.__minimax_alpha_beta(board, 4, -9999, 9999, player,False, dt)
        else:
            result = self.__minimax_alpha_beta(board, 5, -9999, 9999, player,True, dt)
        if result[0]:
            self.preState = copy.deepcopy(board.make_move(result[0][0],result[0][1],player).state)
        return result[0]

