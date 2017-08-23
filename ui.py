import pygame

class UI:
    def __init__(self, appRef):
        self.appRef = appRef
        pygame.font.init()
        self.font = pygame.font.Font("font/FiraCode-Retina.ttf", 46)
    def render(self):
        health = self.appRef.player.health * 2.55
        pygame.draw.rect(self.appRef.draw_surface,(255-health,health,0),(50,50,3 * health,50))
        message = "Lookin Good!" if health > 200 else "Still fine" if health > 150 else "Heal soon!" if health > 50 else "You're almost dead!"
        self.appRef.draw_surface.blit(self.font.render(message, True, (125,220,10)), (10, 10))