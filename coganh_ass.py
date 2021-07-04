import random
import copy
class pre:
    preBoard =[ ]
def evaluate(board,player):
    score = 0
    for i in range(5):
        for j in range(5):
            if board[i][j]==player:
                score+=1
    return 2*score - 16 
def board_print(board, move=()):
    
    print("====== The current board is : ======")
    if move:
        print("move = ", move)
    for i in range(5):
        print(4-i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")
def checkGanhOfBAY(board,pos,player):
    i = pos[0]
    j = pos[1]
    if (i+j)%2==0:
        if conditionMove((i+1,j+1)) and conditionMove((i-1,j-1)):
            if board[i+1][j+1] == board[i-1][j-1] and board[i+1][j+1] == player:
                return True
        if conditionMove((i-1,j+1)) and conditionMove((i+1,j-1)):
            if board[i-1][j+1] == board[i+1][j-1] and board[i+1][j-1] == player:
                return True
    if conditionMove((i+1,j)) and conditionMove((i-1,j)):
        if board[i+1][j] == board[i-1][j] and board[i+1][j] == player:
            return True
    if conditionMove((i,j+1)) and conditionMove((i,j-1)):
        if board[i][j+1] == board[i][j-1] and board[i][j+1] == player:
            return True
    
    return False
def checkBAY(pre,curr):
    dt = [[0,0],[0,0]]
    player = 1
    if evaluate(pre,1) == evaluate(curr,1):
        for i in range(0,5):
            for j in range(0,5):
                if pre[i][j]!=curr[i][j]:
                    if curr[i][j]==0:
                        player = pre[i][j]
                        dt = [[i,j],dt[1]]
                    elif pre[i][j] == 0:
                        player = curr[i][j]
                        dt = [dt[0],[i,j]]
    if dt[0]!=dt[1] and checkGanhOfBAY(curr,dt[0],player):
        return dt
    return [[0,0],[0,0]]
def move(board, player):
    dt = [[0,0],[0,0]]
    if pre.preBoard==[]:
        pre.preBoard = copy.deepcopy(board)
        dt = checkBAY(board,board)
    else:
        dt = checkBAY(pre.preBoard,board)
    if dt[0]!=dt[1]:
        result = minimax_alpha_beta(board, 2, -9999, 9999, player,False, dt)
    else:
        result = minimax_alpha_beta(board, 3, -9999, 9999, player,True, dt)
    if result[0]:
        pre.preBoard = copy.deepcopy(make_move(board,result[0][0],result[0][1],player))
    return result[0]
def conditionPos(board,move,n):
    if move[0]>=0 and move[0]<=4 and move[1]>=0 and move[1]<=4 and board[move[0]][move[1]]==n:
        return True
    return False
def conditionMove(move):
    if not (move[0]>=0 and move[0]<=4 and move[1]>=0 and move[1]<=4):
        return False
    return True
def getAllAvailableMoves(board,player,dt):
    if dt[0]!=dt[1]:
        availableBayMoves = list()
        k = list()
        i,j = dt[0][0],dt[0][1]
        lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
        if (i+j)%2==0:
            lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
        for move in lst:
            if conditionMove(move) and checkGanhOfBAY(board,(i,j),-player): 
                if board[move[0]][move[1]] == player:
                    availableBayMoves.append((move,(i,j)))
        if len(availableBayMoves)>0:
            return availableBayMoves
    availableMoves = list()
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j] == player:
                lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
                if (i+j)%2==0:
                    lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
                for move in lst:
                    if conditionPos(board, move,0):
                        availableMoves.append(((i,j),move))
    return availableMoves
def is_end(board,player):
    count = 0
    lst = getAllAvailableMoves(board,player,[[0,0],[0,0]])
    if len(lst)==0:
        return True
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j] == player:
                count = count + 1

    if count in [0,16]:
        return True
    
    return False
def minimax_alpha_beta(board, depth, alpha, beta, player,isOptimizer,dt):
    if depth == 0 or is_end(board,player):
        return None, evaluate(board,-player)
    best_move = None
    Eval = -9999 if isOptimizer else 9999
    for move in getAllAvailableMoves(board,player,dt):
        new_boardt = copy.deepcopy(board)
        new_board = copy.deepcopy(make_move(new_boardt,move[0], move[1],player))
        m = checkBAY(board,new_board)
        currEval = minimax_alpha_beta(new_board, depth - 1, alpha, beta,-player,not isOptimizer,m)[1]
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
def checkVAY(board,pos,player):
    i = pos[0]
    j = pos[1]
    lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
    if (i+j)%2==0:
        lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
    lst = [l for l in lst if conditionMove(l)]
    for k in lst:
        if board[k[0]][k[1]]==0:
            return False
        if board[k[0]][k[1]]==player:
            mboard = copy.deepcopy(board)
            mboard[pos[0]][pos[1]] = -player
            if not checkVAY(mboard,k,player):
                return False
    return True
def moveVAY(board,pos,player):
    tboard = copy.deepcopy(board)
    tboard[pos[0]][pos[1]] = -player
    i = pos[0]
    j = pos[1]
    lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
    if (i+j)%2==0:
        lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
    lst = [l for l in lst if conditionMove(l)]
    for k in lst:
        if tboard[k[0]][k[1]]==player:
            tboard[k[0]][k[1]] = -player 
            tboard = moveVAY(tboard,k,player)
    return tboard
def make_move(board,startmove,nextmove,player):
    tempBoard = copy.deepcopy(board)
    tempBoard[nextmove[0]][nextmove[1]] = player
    tempBoard[startmove[0]][startmove[1]] = 0
    #GANH
    i = nextmove[0]
    j = nextmove[1]
    lst = []
    if (i+j)%2==0:
        if conditionMove((i+1,j+1)) and conditionMove((i-1,j-1)):
            if tempBoard[i+1][j+1] == tempBoard[i-1][j-1] and tempBoard[i+1][j+1] == -player:
                lst.append((i+1,j+1))
                lst.append((i-1,j-1))
                if checkVAY(tempBoard,(i+1,j+1),-player):
                    tempBoard = moveVAY(tempBoard,(i+1,j+1),-player)
                if checkVAY(tempBoard,(i-1,j-1),-player):
                    tempBoard = moveVAY(tempBoard,(i-1,j-1),-player)
                tempBoard[i+1][j+1] = player
                tempBoard[i-1][j-1] = player
        if conditionMove((i-1,j+1)) and conditionMove((i+1,j-1)):
            if tempBoard[i-1][j+1] == tempBoard[i+1][j-1] and tempBoard[i+1][j-1] == -player:
                lst.append((i-1,j+1))
                lst.append((i+1,j-1))
                if checkVAY(tempBoard,(i-1,j+1),-player):
                    tempBoard = moveVAY(tempBoard,(i-1,j+1),-player)
                if checkVAY(tempBoard,(i+1,j-1),-player):
                    tempBoard = moveVAY(tempBoard,(i+1,j-1),-player)
                tempBoard[i-1][j+1] = player
                tempBoard[i+1][j-1] = player
    if conditionMove((i+1,j)) and conditionMove((i-1,j)):
        if tempBoard[i+1][j] == tempBoard[i-1][j] and tempBoard[i+1][j] == -player:
            lst.append((i+1,j))
            lst.append((i-1,j))
            if checkVAY(tempBoard,(i+1,j),-player):
                tempBoard = moveVAY(tempBoard,(i+1,j),-player)
            if checkVAY(tempBoard,(i-1,j),-player):
                tempBoard = moveVAY(tempBoard,(i-1,j),-player)
            tempBoard[i+1][j] = player
            tempBoard[i-1][j] = player
    if conditionMove((i,j+1)) and conditionMove((i,j-1)):
        if tempBoard[i][j+1] == tempBoard[i][j-1] and tempBoard[i][j+1] == -player:
            lst.append((i,j+1))
            lst.append((i,j-1))
            if checkVAY(tempBoard,(i,j+1),-player):
                tempBoard = moveVAY(tempBoard,(i,j+1),-player)
            if checkVAY(tempBoard,(i,j-1),-player):
                tempBoard = moveVAY(tempBoard,(i,j-1),-player)
            tempBoard[i][j+1] = player
            tempBoard[i][j-1] = player

    #VAY
    for k in lst:
        tempBoard = copy.deepcopy(VAY(tempBoard,k,player))
    tempBoard = VAY(tempBoard,(i,j),player)
    return tempBoard
def VAY(board,pos,player):
    i,j =pos[0],pos[1]
    tempBoard = copy.deepcopy(board)
    lst = [z for z in [(i-1,j),(i,j-1),(i,j+1),(i+1,j)] if conditionPos(tempBoard,z,-player)]
    if (i+j)%2==0:
        lst = [z for z in [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)] if conditionPos(tempBoard,z,-player)]
    for l in lst:
        if checkVAY(tempBoard,l,-player):
            tempBoard = moveVAY(tempBoard,l,-player)
    return tempBoard

def main():
    board =[
        [-1, 0,-1, 1,-1],
        [ 0, 0,-1,-1, 0],
        [ 1, 0, 1, 0,-1],
        [ 1,-1, 1, 0, 0],
        [ 1, 1, 0, 0,-1]
    ]
    print(move(board,1))


import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
