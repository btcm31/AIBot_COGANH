from board import Board
from bot import Bot
import copy
def play():
    bot = Bot(90)
    board = Board([[-1,-1,-1,-1,-1],[-1, 0, 0, 0,-1],[ 1, 0, 0, 0,-1],[ 1, 0, 0, 0, 1],[ 1, 1, 1, 1, 1]])
    player = 1
    board.board_print()
    while not board.is_end(player):
        tBoard = Board(board.state)
        move = ()
        if player == 1:
            mstart = tuple(map(lambda x: int(x), input("Input start point: ").split(" ")))
            while not board.conditionPos(mstart,player):
                mstart = tuple(map(lambda x: int(x), input("Input start point again: ").split(" ")))
            mend = tuple(map(lambda x: int(x), input("Input end point: ").split(" ")))
            while not board.conditionPos(mend,0):
                mend = tuple(map(lambda x: int(x), input("Input end point again: ").split(" ")))
            move = (mstart, mend)
            board.state = board.make_move(mstart, mend , 1)
        else:
            move = bot.move(tBoard,player)
            board.state = copy.deepcopy(board.make_move(move[0], move[1] , 1))

        board.board_print(move)
        player = -player

if __name__ == "__main__":
    play()
