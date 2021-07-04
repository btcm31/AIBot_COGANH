from board import Board
from bot import Bot
import copy
def play():
    bot = Bot(90)
    board = Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]])
    player = 1
    board.board_print()
    while not board.is_end(player):
        move = ()
        if player == 1:

            mstart = tuple(map(lambda x: int(x), input("Input start point: ").split(" ")))
            while not board.conditionPos(mstart,player):
                mstart = tuple(map(lambda x: int(x), input("Input start point again: ").split(" ")))

            lstNext = [point[1] for point in board.getAllAvailableMoves(player,(0,0)) if point[0]==mstart]


            mend = tuple(map(lambda x: int(x), input("Input end point: ").split(" ")))
            while mend not in lstNext:
                mend = tuple(map(lambda x: int(x), input("Endpoint is invalid! Again: ").split(" ")))

            move = (mstart, mend)
            board = copy.deepcopy(board.make_move(mstart, mend , player))

            
        else:
            move = bot.move(board,player)
            board = copy.deepcopy(board.make_move(move[0], move[1] , player))

        board.board_print(move)
        player = -player

if __name__ == "__main__":
    play()
