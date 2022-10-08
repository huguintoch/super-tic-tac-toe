import sys
import pygame
from game import SuperBoard, Player
from ai import SuperTicTacToeGameController
from easyAI import Human_Player, AI_Player, Negamax
from pygame.locals import *

#Global Variables
HEIGHT = 450
WIDTH = HEIGHT
FPS = 15
VECTOR2 = pygame.math.Vector2  # 2 for two dimensional
BACKGROUND_COLOR = (255, 255, 255)

#PYGAME USER EVENTS
AIACTION = pygame.USEREVENT+1

def processTile(superBoard, board, tile, playerColor):
    global activePlayer
    if tile.switchState(playerColor):
        if board.checkWin():
            print("Board: " + str(board.boardIndex) + " won by " + str(playerColor))
            board.winBoard(playerColor)
            if superBoard.checkWin():
                print("Game won by Player " + str(playerColor))
                sys.exit()
        if board.isFull() and not board.isWon:
            board.reset()
        
        for board2 in superBoard.boards:
            if board2.boardIndex == tile.tileIndex:
                board2.isActive = True
                if board2.isWon:
                    for board3 in superBoard.boards:
                        board3.isActive = True
                    break
            else:
                board2.isActive = False

        activePlayer = (activePlayer + 1) % 2
        #return True

    else: return False

def main():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.display.set_caption("SuperTicTacToe")

    superBoard = SuperBoard(HEIGHT)
    players = [Player(1, True), Player(2, False)]
    ai_players = [AI_Player(Negamax(4)), Human_Player()]
    superBoardController = SuperTicTacToeGameController(ai_players)
    global activePlayer
    activePlayer = 0
    while True:
        if players[activePlayer].isAi:
            pygame.event.post(pygame.event.Event(AIACTION, {"player":activePlayer}))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not players[activePlayer].isAi:
            for boardIndex, board in enumerate(superBoard.boards):
                if board.isActive:
                    for tileIndex, tile in enumerate(board.tiles):
                        if tile.rect.collidepoint(event.pos):
                            superBoardController.play_move(move = (boardIndex, tileIndex))
                            processTile(superBoard, board, tile, players[activePlayer].color)
        if event.type == AIACTION:
            newAction = superBoardController.get_move()
            superBoardController.play_move(move = newAction)
            processTile(superBoard, superBoard.boards[newAction[0]], superBoard.boards[newAction[0]].tiles[newAction[1]], players[activePlayer].color)
            pass
                            
        superBoard.render(screen)

        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT/3), (WIDTH, HEIGHT/3), 3)
        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT*2/3), (WIDTH, HEIGHT*2/3), 3)
        pygame.draw.line(screen, (0, 0, 0), (WIDTH/3, 0), (WIDTH/3, HEIGHT), 3)
        pygame.draw.line(screen, (0, 0, 0), (WIDTH*2/3, 0), (WIDTH*2/3, HEIGHT), 3)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
