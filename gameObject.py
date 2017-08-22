"""object controls and stuff"""
import pygame

class Object:
    """see top"""
    def __init__(self, appRef, x = 0, y = 0, xsize = 100, ysize = 100):
        self.appRef = appRef
        self.size = xsize, ysize
        self.velocity = 0, 0
        self.position = (x, y)
        self.sprite = pygame.image.load("tex/object.jpg").convert()
        self.sprite = pygame.transform.scale(self.sprite, self.size)
    def render(self):
        x, y = self.position
        self.appRef.display_surface.blit(self.sprite, (x - self.appRef.offset[0], (self.appRef.size[1] - self.size[1])-(y - self.appRef.offset[1])))
