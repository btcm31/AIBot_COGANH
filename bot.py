import random
import copy
from board import Board
import time

class Bot:
    def __init__(self,remaintime):
        self.remaintime = remaintime
        self.preState = []
    def __minimax_alpha_beta(self, board:Board, depth, alpha, beta, player,isOptimizer,dt):
        temp = Board(board.state)
        if depth == 0 or board.is_end(player)[0]:
            return None, board.evaluate(-player)
        best_movelst = []
        Eval = -9999 if isOptimizer else 9999
        for move in board.getAllAvailableMoves(player,dt):
            new_board = copy.deepcopy(board.make_move(move[0], move[1],player))
            m = board.checkBAY(board,new_board)
            currEval = self.__minimax_alpha_beta(new_board, depth - 1, alpha, beta,-player,not isOptimizer,m)[1]
            if isOptimizer and Eval <= currEval:
                Eval = currEval
                best_movelst.append((move,Eval))
                alpha = max(alpha, Eval)
                if beta <= alpha:
                    break
            elif not isOptimizer and Eval >= currEval:
                Eval = currEval
                best_movelst.append((move,Eval))
                beta = min(beta, Eval)
                if beta <= alpha:
                    break
        lst = [i[0] for i in best_movelst if i[1]==Eval]
        best_move = lst[random.randint(0, len(lst) - 1)]
        return best_move, Eval
    def move(self, board:Board, player):
        startT = time.time()
        dt = [[0,0],[0,0]]
        if self.preState==[]:
            m = Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]])
            dt = board.checkBAY(m,board)
        else:
            dt = board.checkBAY(Board(self.preState),board)
        if dt[0]!=dt[1]:
            result = self.__minimax_alpha_beta(board, 2, -9999, 9999, player, False, dt)
        else:
            depth = 5
            if board.evaluate(player)>=12:
                depth = 1
            elif board.evaluate(player)>=8:
                depth = 3
            elif board.evaluate(player) <= -10:
                depth = 2
            result = self.__minimax_alpha_beta(board, depth, -9999, 9999, player, True, dt)
        if result[0]:
            self.preState = copy.deepcopy(board.make_move(result[0][0],result[0][1],player).state)
        self.remaintime = self.remaintime - (time.time() - startT)
        return result[0]

