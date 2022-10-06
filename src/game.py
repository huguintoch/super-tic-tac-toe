import pygame
from enum import Enum

#Definiendocolores de cada tile
TILE_COLORS = [(255, 255, 255), (255, 0, 0), (0, 0, 255)]  # Vacio, Rojo, Azul


class Tile(pygame.sprite.Sprite):

    def __init__(self, sideLength, tileIndex, boardPos):

        super().__init__()

        self.state = 0
        self.tileIndex = tileIndex
        self.image = pygame.Surface([sideLength, sideLength])
        self.image.fill(TILE_COLORS[self.state])
        self.rect = self.image.get_rect()
        self.rect.x = sideLength * (tileIndex % 3) + boardPos.x
        self.rect.y = sideLength * (int)(tileIndex / 3) + boardPos.y

    def switchState(self, newState) -> bool:
        if self.state != 0:
            return False
        self.state = newState
        self.image.fill(TILE_COLORS[self.state])
        return True
    
    def winState(self, winState):
        self.state = winState
        self.image.fill(TILE_COLORS[self.state])

    def render(self, board: pygame.Surface):
        board.blit(self.image, self.rect)


class Board(pygame.sprite.Sprite):

    def __init__(self, sideLength, boardIndex):
        super().__init__()
        self.image = pygame.Surface([sideLength, sideLength])
        self.image.fill((255/9, 255, 255))
        self.boardIndex = boardIndex
        self.rect = self.image.get_rect()
        self.rect.x = sideLength * (boardIndex % 3)
        self.rect.y = sideLength * (int)(boardIndex / 3)
        self.tiles = [Tile(sideLength/3, 0, self.rect), Tile(sideLength/3, 1, self.rect), Tile(sideLength/3, 2, self.rect),
                      Tile(sideLength/3, 3, self.rect), Tile(sideLength/3,
                                                             4, self.rect), Tile(sideLength/3, 5, self.rect),
                      Tile(sideLength/3, 6, self.rect), Tile(sideLength/3, 7, self.rect), Tile(sideLength/3, 8, self.rect)]

    def renderLines(self, screen: pygame.Surface):

        height = self.rect.height + self.rect.y
        height1 = self.rect.height/3 + self.rect.y
        height2 = self.rect.height*2/3 + self.rect.y

        width = self.rect.width + self.rect.x
        width1 = self.rect.width/3 + self.rect.x
        width2 = self.rect.width*2/3 + self.rect.x

        pygame.draw.line(screen, (0, 0, 0), (0, height1), (width, height1), 1)
        pygame.draw.line(screen, (0, 0, 0), (0, height2), (width, height2), 1)
        pygame.draw.line(screen, (0, 0, 0), (width1, 0), (width1, height), 1)
        pygame.draw.line(screen, (0, 0, 0), (width2, 0), (width2, height), 1)

    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        for tile in self.tiles:
            tile.render(screen)
        self.renderLines(screen)
    
    def checkWin(self) -> bool:
        firstRow    = self.tiles[0].state == self.tiles[1].state and self.tiles[1].state == self.tiles[2].state and self.tiles[0].state != 0
        secondRow   = self.tiles[3].state == self.tiles[4].state and self.tiles[4].state == self.tiles[5].state and self.tiles[3].state != 0
        thirdRow    = self.tiles[6].state == self.tiles[7].state and self.tiles[7].state == self.tiles[8].state and self.tiles[6].state != 0

        firstColumn     = self.tiles[0].state == self.tiles[3].state and self.tiles[3].state == self.tiles[6].state and self.tiles[0].state != 0
        secondColumn    = self.tiles[1].state == self.tiles[4].state and self.tiles[4].state == self.tiles[7].state and self.tiles[1].state != 0
        thirdColumn     = self.tiles[2].state == self.tiles[5].state and self.tiles[5].state == self.tiles[8].state and self.tiles[2].state != 0

        firstDiag       = self.tiles[0].state == self.tiles[4].state and self.tiles[4].state == self.tiles[8].state and self.tiles[0].state != 0
        secondDiag      = self.tiles[2].state == self.tiles[4].state and self.tiles[4].state == self.tiles[6].state and self.tiles[2].state != 0

        return firstRow | firstColumn | firstDiag | secondRow | secondColumn | secondDiag | thirdRow | thirdColumn
    
    def winBoard(self, winningPlayer):
        for tile in self.tiles:
            tile.winState(winningPlayer)



class SuperBoard:
    def __init__(self, sideLength):
        self.boards = [Board(sideLength/3, 0), Board(sideLength/3, 1), Board(sideLength/3, 2),
                       Board(sideLength/3, 3), Board(sideLength /
                                                     3, 4), Board(sideLength/3, 5),
                       Board(sideLength/3, 6), Board(sideLength/3, 7), Board(sideLength/3, 8)]

    def render(self, screen: pygame.Surface):
        for board in self.boards:
            board.render(screen)

class Player:
    def __init__(self, color: int, isAI: bool = False):
        self.isAi = isAI
        self.color = color