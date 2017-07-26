"""player controls and stuff"""
import pygame

class Player:
    """see top"""
    def __init__(self, appRef, x = 0, y = 0):
        self.appRef = appRef
        self.size = 100, 100
        self.velocity = 0, 0
        self.position = (x, y)
        self.sprite = pygame.image.load("tex/glider.jpg").convert()
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.onGround = False
    def move(self, pos):
        x, y = pos
        if self.onGround:
            self.velocity = self.velocity[0] * 0.95, self.velocity[1]
        else:
            self.velocity = self.velocity[0], self.velocity[1]-9.8*0.004
            x = 0
            y = 0
        x += self.velocity[0]
        y += self.velocity[1]
        self.velocity = x, y
        newpos = (x + self.position[0], y + self.position[1])
        ybound = self.appRef.size[1] - self.size[1]
        xbound = self.appRef.size[0] - self.size[0]
        if newpos[0] < 0:
            newpos = 0, newpos[1]
        if newpos[1] < 0:
            newpos = newpos[0], 0
            self.onGround = True
            self.velocity = self.velocity[0], 0
        else:
            self.onGround = False            
        if newpos[0] > xbound:
            newpos = xbound, newpos[1]
        if newpos[1] > ybound:
            newpos = newpos[0], ybound
        self.position = newpos
    def render(self, surface):
        x, y = self.position
        surface.blit(self.sprite, (x, (self.appRef.size[1] - self.size[1])-y))
