import pygame as pg
from constants import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DrawingTile:
    def __init__(self, pos, size):
        self.rect = pg.Rect(pos.x, pos.y, size, size)
        self.color = WHITE
    
    def changeColor(self):
        if self.color == BLACK:
            self.color = WHITE
        if self.color == WHITE:
            self.color = BLACK
    
    def draw(self, WIN):
        pg.draw.rect(WIN, self.color, self.rect)
    

class DrawingGrid:
    def __init__(self, pos, dimension, tileSize = 30):
        self.pos = pos

        self.grid = []
        for i in range(dimension[1]):
            row = []
            for j in range(dimension[0]):
                row.append(DrawingTile(Point(pos.x + (j * tileSize), pos.y + (i * tileSize)), tileSize))
            self.grid.append(row)
        
        self.drawing = False

    def update(self, events):
        
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.drawing = True
            if event.type == pg.MOUSEBUTTONUP:
                self.drawing = False
        
        if self.drawing:
            for row in self.grid:
                for tile in row:
                    if tile.rect.collidepoint(pg.mouse.get_pos()):
                        tile.changeColor()

    def draw(self, WIN):
        for row in self.grid:
            for tile in row:
                tile.draw(WIN)
    
    def generateMap(self):
        map = []
        for row in self.grid:
            for tile in row:
                if tile.color == WHITE:
                    map.append(1)
                if tile.color == BLACK:
                    map.append(0)
        
        return map

    def resetGrid(self):
        for row in self.grid:
            for tile in row:
                tile.color = WHITE