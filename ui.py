import pygame as pg
from constants import *

class UIElement:
    def __init__(self, pos, color=WHITE, centerX=None, centerY=None):
        self.x = pos[0]
        self.y = pos[1]
        self.color = color

        self.centerX = centerX
        self.centerY = centerY

        self.rect = pg.Rect(self.x, self.y, 0, 0)

    def update(self):
        if self.centerX != None:
            self.x = ((self.centerX[0] + self.centerX[1]) / 2) - (self.rect.width / 2)
            self.rect.x = self.x
        if self.centerY != None:
            self.y = ((self.centerY[0] + self.centerY[1]) / 2) - (self.rect.height / 2)
            self.rect.y = self.y

    def draw(self, WIN):
        pass

    def eventHandler(self, event):
        pass

class Text(UIElement):
    def __init__(self, text, pos, color=BACKGROUND, textColor=WHITE, font=None, fontSize=36, textUpdate=None, centerX=None, centerY=None):
        super().__init__(pos, color=color, centerX=centerX, centerY=centerY)

        self.text = text
        self.textColor = textColor
        self.font = pg.font.SysFont(font, fontSize)
        self.textUpdate = textUpdate

        img = self.font.render(self.text, True, self.textColor)
        self.rect = pg.Rect(self.x - 5, self.y - 2.5, img.get_rect().width + 10, img.get_rect().height + 5)

    def draw(self, WIN):
        img = self.font.render(self.text, True, self.textColor)
        pg.draw.rect(WIN, self.color, self.rect, border_radius=10)
        WIN.blit(img, (self.x, self.y))
    
    def update(self):
        super().update()
        if self.textUpdate != None:
            self.text = self.textUpdate()
    
    def center(self, minX=0, maxX=WIDTH):
        self.x = ((minX + maxX) / 2) - (self.rect.width / 2)

class Button(Text):
    def __init__(self, text, pos, callback, color=BACKGROUND, textColor=WHITE, font=None, fontSize=36, centerX=None, centerY=None):
        super().__init__(text, pos, color=color, textColor=textColor, font=font, fontSize=fontSize, centerX=centerX, centerY=centerY)
        
        self.callback = callback

    def eventHandler(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.callback()

class Window:
    def __init__(self, manager, initialUIRegister=[], background=None, loadCallback=None):
        self.UI_REGISTER = initialUIRegister
        self.BACKGROUND = background

        self.loadCallback = loadCallback

        manager.WINDOW_REGISTER.append(self)

    def addElement(self, element):
        self.UI_REGISTER.append(element)

    def update(self):
        for element in self.UI_REGISTER:
            element.update()
    
    def draw(self, WIN):
        if self.BACKGROUND != None:
            WIN.fill(self.BACKGROUND)

        for element in self.UI_REGISTER:
            element.draw(WIN)
    
    def eventHandler(self, events):
        for element in self.UI_REGISTER:
            element.eventHandler(events)

class WindowManager:
    def __init__(self, WIN):
        self.WINDOW_REGISTER = [None]
        self.ACTIVE_WINDOW = self.WINDOW_REGISTER[0]

        self.WIN = WIN
    
    def update(self, events):
        if self.ACTIVE_WINDOW != None:
            self.ACTIVE_WINDOW.update()
            self.ACTIVE_WINDOW.draw(self.WIN)
            self.ACTIVE_WINDOW.eventHandler(events)
    
    def setActiveWindow(self, index):
        self.ACTIVE_WINDOW = self.WINDOW_REGISTER[index]
        if self.ACTIVE_WINDOW.loadCallback != None:
            self.ACTIVE_WINDOW.loadCallback()

        if index == 0:
            self.WIN.fill(BACKGROUND)
