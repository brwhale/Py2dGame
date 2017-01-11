"""Simple 2d game thing in python"""
import pygame
# pylint: disable=W0614
# pylint: disable=W0401
from pygame.locals import *
import events
import player

class App(events.CEvent):
    """main class for game"""
    def __init__(self):
        """window init"""
        self._running = True
        self.display_surface = None
        self.size = self.weight, self.height = 1280, 720
    def on_init(self):
        """game init"""
        # pylint: disable=E1101
        # pylint: disable=W0201
        pygame.init()
        pygame.display.set_caption("snek 2d 0.1")
        self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.player = player.Player(50, 60)
    def on_loop(self):
        """game logic here"""
        self.player.move(self.getInputMove())
    def on_render(self):
        """render stuff here"""
        self.display_surface.fill((0,0,0))
        self.player.render(self.display_surface)
        pygame.display.flip()
    def on_cleanup(self):
        """quittin time"""
        # pylint: disable=E1101
        pygame.quit()
    def on_exit(self):
        self._running = False
    def on_execute(self):
        """start the main loop"""
        # pylint: disable=C0121
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    App().on_execute()
