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


def main():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.display.set_caption("SuperTicTacToe")

    superBoard = SuperBoard(HEIGHT)
    players = [Player(1), Player(2)]
    activePlayer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not players[activePlayer].isAi:
            for board in superBoard.boards:
                for tile in board.tiles:
                    if tile.rect.collidepoint(event.pos):
                        if tile.switchState(players[activePlayer].color):
                            activePlayer = (activePlayer + 1) % 2
        
        superBoard.render(screen)
        
        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT/3),
                         (WIDTH, HEIGHT/3), 3)
        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT*2/3),
                         (WIDTH, HEIGHT*2/3), 3)
        pygame.draw.line(screen, (0, 0, 0), (WIDTH/3, 0), (WIDTH/3, HEIGHT), 3)
        pygame.draw.line(screen, (0, 0, 0), (WIDTH*2/3, 0),
                         (WIDTH*2/3, HEIGHT), 3)
        pygame.display.update()


if __name__ == '__main__':
    main()
