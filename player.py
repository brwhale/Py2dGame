"""player controls and stuff"""
import pygame

class Player:
    """see top"""
    def __init__(self, x = 0, y = 0):
        self.position = (x, y)
        self.sprite = pygame.image.load("tex/glider.jpg").convert()
    def move(self, pos):
        x, y = pos
        self.position = (x + self.position[0], y + self.position[1])
    def render(self, surface):
        x, y = self.position
        y *= -1
        surface.blit(self.sprite, (x, y))
