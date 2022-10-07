import sys
import pygame
from game import SuperBoard, Player
from pygame.locals import *

#Global Variables
HEIGHT = 450
WIDTH = HEIGHT
FPS = 15
VECTOR2 = pygame.math.Vector2  # 2 for two dimensional
BACKGROUND_COLOR = (255, 255, 255)

def processTile(superBoard, board, tile, players):
    global activePlayer
    if tile.switchState(players[activePlayer].color):
        print(tile)
        if board.checkWin():
            print("Board: " + str(board.boardIndex) + " won by " + str(players[activePlayer].color))
            board.winBoard(players[activePlayer].color)
            if superBoard.checkWin():
                print("Game won by Player " + str(players[activePlayer].color))
                sys.exit()
        if board.isFull() and not board.isWon:
            board.reset()
        
        for board2 in superBoard.boards:
            if board2.boardIndex == tile.tileIndex:
                board2.active = True
                if board2.isWon:
                    for board3 in superBoard.boards:
                        board3.active=True
                    break
            else:
                board2.active = False

        activePlayer = (activePlayer + 1) % 2

def main():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.display.set_caption("SuperTicTacToe")

    superBoard = SuperBoard(HEIGHT)
    players = [Player(1), Player(2)]
    global activePlayer
    activePlayer = 0
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not players[activePlayer].isAi:
            for board in superBoard.boards:
                if board.active:
                    for tile in board.tiles:
                        if tile.rect.collidepoint(event.pos):
                            processTile(superBoard, board, tile, players)
                            
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
