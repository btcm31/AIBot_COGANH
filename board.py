import random
import copy

class Board:
    def __init__(self,state):
        self.state = state

    def evaluate(self,player):
        score = 0
        for i in range(5):
            for j in range(5):
                if self.state[i][j] == player:
                    score+=1
        return 2*score - 16
    def getAllAvailableMoves(self,player,dt):
        if dt[0]!=dt[1]:
            availableBayMoves = list()
            k = list()
            i,j = dt[0][0],dt[0][1]
            lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
            if (i+j)%2==0:
                lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
            for move in lst:
                if self.conditionMove(move) and self.checkGanhOfBAY((i,j),-player): 
                    if self.state[move[0]][move[1]] == player:
                        availableBayMoves.append((move,(i,j)))
            if len(availableBayMoves)>0:
                return availableBayMoves
        availableMoves = list()
        for i in range(0,5):
            for j in range(0,5):
                if self.state[i][j] == player:
                    lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
                    if (i+j)%2==0:
                        lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
                    for move in lst:
                        if self.conditionPos(move,0):
                            availableMoves.append(((i,j),move))
        return availableMoves
    def conditionPos(self,move,n):
        if move[0]>=0 and move[0]<=4 and move[1]>=0 and move[1]<=4 and self.state[move[0]][move[1]]==n:
            return True
        return False
    def conditionMove(self,move):
        if not (move[0]>=0 and move[0]<=4 and move[1]>=0 and move[1]<=4):
            return False
        return True
    def is_end(self,player):
        count = 0
        lst = self.getAllAvailableMoves(player,[[0,0],[0,0]])
        if len(lst)==0:
            return True
        for i in range(0,5):
            for j in range(0,5):
                if self.state[i][j] == player:
                    count = count + 1

        if count in [0,16]:
            return True
        
        return False
    def board_print(self, move=()):
        
        print("====== The current board is : ======")
        print("   ", " 0", " 1", " 2", " 3", " 4")
        if move:
            print("move = ", move)
        for i in range(5):
            print(i, ":", end=" ")
            for j in range(5):
                print(" "*(0 if self.state[i][j]==-1 else 1) + str(self.state[i][j]), end=" ")
            print()
        
        print("")

    def checkGanhOfBAY(self, pos,player):
        i = pos[0]
        j = pos[1]
        if (i+j)%2==0:
            if self.conditionMove((i+1,j+1)) and self.conditionMove((i-1,j-1)):
                if self.state[i+1][j+1] == self.state[i-1][j-1] and self.state[i+1][j+1] == player:
                    return True
            if self.conditionMove((i-1,j+1)) and self.conditionMove((i+1,j-1)):
                if self.state[i-1][j+1] == self.state[i+1][j-1] and self.state[i+1][j-1] == player:
                    return True
        if self.conditionMove((i+1,j)) and self.conditionMove((i-1,j)):
            if self.state[i+1][j] == self.state[i-1][j] and self.state[i+1][j] == player:
                return True
        if self.conditionMove((i,j+1)) and self.conditionMove((i,j-1)):
            if self.state[i][j+1] == self.state[i][j-1] and self.state[i][j+1] == player:
                return True
        return False
    def checkBAY(self, pre, curr):
        dt = [[0,0],[0,0]]
        player = 1

        if pre.evaluate(1) == curr.evaluate(1): 
            for i in range(0,5):
                for j in range(0,5):
                    if pre.state[i][j]!=curr.state[i][j]:
                        if curr.state[i][j]==0:
                            player = pre.state[i][j]
                            dt = [[i,j],dt[1]]
                        elif pre.state[i][j] == 0:
                            player = curr.state[i][j]
                            dt = [dt[0],[i,j]]
        if dt[0]!=dt[1] and curr.checkGanhOfBAY(dt[0],player):
            return dt
        return [[0,0],[0,0]]
    def checkVAY(self, pos, player):
        i = pos[0]
        j = pos[1]
        lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
        if (i+j)%2==0:
            lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
        lst = [l for l in lst if self.conditionMove(l)]
        for k in lst:
            if self.state[k[0]][k[1]]==0:
                return False
            if self.state[k[0]][k[1]]==player:
                mboard = Board(self.state)
                mboard.state[pos[0]][pos[1]] = -player
                if not mboard.checkVAY(k,player):
                    return False
        return True
    def moveVAY(self, pos, player):
        tboard = Board(self.state)
        tboard.state[pos[0]][pos[1]] = -player
        i = pos[0]
        j = pos[1]
        lst = [(i-1,j),(i,j-1),(i,j+1),(i+1,j)]
        if (i+j)%2==0:
            lst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)]
        lst = [l for l in lst if self.conditionMove(l)]
        for k in lst:
            if tboard.state[k[0]][k[1]]==player:
                tboard.state[k[0]][k[1]] = -player 
                tboard.state = copy.deepcopy(tboard.moveVAY(k,player))
        return tboard.state
    def make_move(self, startmove, nextmove, player):
        tempBoard = Board(self.state)
        tempBoard.state[nextmove[0]][nextmove[1]] = player
        tempBoard.state[startmove[0]][startmove[1]] = 0
        #GANH
        i = nextmove[0]
        j = nextmove[1]
        lst = []
        if (i+j)%2==0:
            if self.conditionMove((i+1,j+1)) and self.conditionMove((i-1,j-1)):
                if tempBoard.state[i+1][j+1] == tempBoard.state[i-1][j-1] and tempBoard.state[i+1][j+1] == -player:
                    lst.append((i+1,j+1))
                    lst.append((i-1,j-1))
                    if tempBoard.checkVAY((i+1,j+1),-player):
                        tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i+1,j+1),-player))
                    if tempBoard.checkVAY((i-1,j-1),-player):
                        tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i-1,j-1),-player))
                    tempBoard.state[i+1][j+1] = player
                    tempBoard.state[i-1][j-1] = player
            if self.conditionMove((i-1,j+1)) and self.conditionMove((i+1,j-1)):
                if tempBoard.state[i-1][j+1] == tempBoard.state[i+1][j-1] and tempBoard.state[i+1][j-1] == -player:
                    lst.append((i-1,j+1))
                    lst.append((i+1,j-1))
                    if tempBoard.checkVAY((i-1,j+1),-player):
                        tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i-1,j+1),-player))
                    if tempBoard.checkVAY((i+1,j-1),-player):
                        tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i+1,j-1),-player))
                    tempBoard.state[i-1][j+1] = player
                    tempBoard.state[i+1][j-1] = player
        if self.conditionMove((i+1,j)) and self.conditionMove((i-1,j)):
            if tempBoard.state[i+1][j] == tempBoard.state[i-1][j] and tempBoard.state[i+1][j] == -player:
                lst.append((i+1,j))
                lst.append((i-1,j))
                if tempBoard.checkVAY((i+1,j),-player):
                    tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i+1,j),-player))
                if tempBoard.checkVAY((i-1,j),-player):
                    tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i-1,j),-player))
                tempBoard.state[i+1][j] = player
                tempBoard.state[i-1][j] = player
        if self.conditionMove((i,j+1)) and self.conditionMove((i,j-1)):
            if tempBoard.state[i][j+1] == tempBoard.state[i][j-1] and tempBoard.state[i][j+1] == -player:
                lst.append((i,j+1))
                lst.append((i,j-1))
                if tempBoard.checkVAY((i,j+1),-player):
                    tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i,j+1),-player))
                if tempBoard.checkVAY((i,j-1),-player):
                    tempBoard.state = copy.deepcopy(tempBoard.moveVAY((i,j-1),-player))
                tempBoard.state[i][j+1] = player
                tempBoard.state[i][j-1] = player

        #VAY
        for k in lst:
            tempBoard.state = copy.deepcopy(tempBoard.VAY(k,player))
        tempBoard = Board(tempBoard.VAY((i,j),player))
        return tempBoard.state
    def VAY(self, pos, player):
        i,j =pos[0],pos[1]
        tempBoard = Board(self.state)
        lst = [z for z in [(i-1,j),(i,j-1),(i,j+1),(i+1,j)] if self.conditionPos(z,-player)]
        if (i+j)%2==0:
            lst = [z for z in [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j),(i+1,j-1),(i+1,j+1)] if self.conditionPos(z,-player)]
        for l in lst:
            if tempBoard.checkVAY(l,-player):
                tempBoard.state = copy.deepcopy(tempBoard.moveVAY(l,-player))
        return tempBoard.state

