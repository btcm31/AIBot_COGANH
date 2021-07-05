from board import Board
from bot import Bot
import copy
import time

def playvsBot():
    bot = Bot(90)
    board = Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]])
    player = 1
    board.board_print()
    youtime = time.time()
    while not board.is_end(player)[0]:
        move = ()
        lstNext = []
        if player == 1:
            while True:
                try:
                    mstart = tuple(map(lambda x: int(x), input("Input start point: ").split(" ")))
                    if not board.conditionPos(mstart,player):
                        print("Invalid start point! Please again")
                        continue
                    lstNext = [point[1] for point in board.getAllAvailableMoves(player,(0,0)) if point[0]==mstart]
                    if len(lstNext)==0:
                        print("Not exist next move! Please again")
                        continue
                except KeyboardInterrupt:
                    break
                except:
                    continue
                else:
                    break
            while True:
                try:
                    mend = tuple(map(lambda x: int(x), input("Input end point: ").split(" ")))
                    if mend not in lstNext:
                        print("Endmove is invalid! Endmove must in %s." % lstNext)
                        continue
                except KeyboardInterrupt:
                    break
                except:
                    continue
                else:
                    break
            if time.time() - youtime > 90:
                print("You timed out!!")
                break
            move = (mstart, mend)
            board = copy.deepcopy(board.make_move(mstart, mend , player))
        else:
            move = bot.move(board,player)
            if bot.remaintime <0 :
                print("Bot timed out!!")
                print("You win!")
                break
            board = copy.deepcopy(board.make_move(move[0], move[1] , player))
        board.board_print(move)
        player = -player
def BotvsBot():
    bot1 = Bot(90)
    bot2 = Bot(90)
    board = Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]])
    player = 1
    board.board_print()
    while not board.is_end(player)[0]:
        move = ()
        if player == 1:
            move = bot1.move(board,player)
            board = copy.deepcopy(board.make_move(move[0], move[1] , player))
            if bot1.remaintime <= 0 :
                print("Bot1 timed out!")
                print("Bot2 win")
                break
            board.Botboard_print(move,1,bot1.remaintime)
        else:
            move = bot2.move(board,player)
            board = copy.deepcopy(board.make_move(move[0], move[1] , player))
            if bot2.remaintime <= 0 :
                print("Bot2 timed out!")
                print("Bot1 win")
                break
            board.Botboard_print(move, 2, bot2.remaintime)
        player = -player
    else:
        if board.is_end(1)[1] == 0:
            print("Bot2 win")
        else: print("Bot1 win")
if __name__ == "__main__":
    mode = input("Choose playvsBot or BotvsBot (1 or other): ")
    if mode == "1":
        print("***You choosed play vs Bot.***")
        playvsBot()
    else: 
        print("***You choosed Bot vs Bot.***")
        BotvsBot()