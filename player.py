"""player controls and stuff"""
import pygame

class Player:
    """see top"""
    def __init__(self, appRef, x = 0, y = 0):
        self.appRef = appRef
        self.size = 100, 100
        self.jumpSpeed = 6.1
        self.runSpeed = 0.1
        self.velocity = 0, 0
        self.position = (x, y)
        self.sprite = pygame.image.load("tex/glider.jpg").convert()
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.onGround = False
        self.renderMode = 0
    def move(self, pos):
        # transform input move vector into character move vector
        x, y = pos[0] * self.runSpeed, 0 if pos[1] < 0 else pos[1] * self.jumpSpeed
        # velocity: add drag if on ground, else add gravity
        if self.onGround:
            self.velocity = self.velocity[0] * 0.95, self.velocity[1]
        else:
            self.velocity = self.velocity[0], self.velocity[1]-9.8*0.004
            x = x * self.runSpeed
            y = 0
        # calculate new position from velocity
        x += self.velocity[0]
        y += self.velocity[1]
        if (y > self.jumpSpeed):
            y = self.jumpSpeed
        self.velocity = x, y
        newpos = (x + self.position[0], y + self.position[1])
        # calculate colisions from new position
        self.onGround = False
        for obj in self.appRef.objects:
            x1 = obj.position[0] - self.size[0]
            x2 = obj.position[0] + obj.size[0] 
            y1 = obj.position[1] - self.size[1]
            y2 = obj.position[1] + obj.size[1]
            if (newpos[0] > x1 and newpos[0] < x2):
                if (newpos[1] > y1 and newpos[1] < y2):
                    x = abs(((newpos[0] - x1) + (newpos[0] - x2)) / (self.size[0] + obj.size[0]))
                    yy = ((newpos[1] - y1) + (newpos[1] - y2)) / (self.size[1] + obj.size[1])
                    y = abs(yy)
                    if (x > y):
                        newpos = self.position[0], newpos[1]
                        self.velocity = 0, self.velocity[1]
                    else:
                        newpos = newpos[0], self.position[1]
                        self.velocity = self.velocity[0], 0
                        if (yy >= 0):
                            self.onGround = True
        # update position taking everyhting into account
        self.position = newpos
    def render(self):
        x, y = self.position
        self.appRef.display_surface.blit(self.sprite, (x, (self.appRef.size[1] - self.size[1])-y), None, self.renderMode)
