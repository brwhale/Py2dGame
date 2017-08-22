"""Simple 2d game thing in python"""
import pygame
# pylint: disable=W0614
# pylint: disable=W0401
from pygame.locals import *
import events
import player
import gameObject

class App(events.CEvent):
    """main class for game"""
    def __init__(self):
        """window init"""
        self._running = True
        self.display_surface = None
        self.size = self.weight, self.height = 1280, 720
        self.offset = 0, 0
    def on_init(self):
        """game init"""
        # pylint: disable=E1101
        # pylint: disable=W0201
        pygame.init()
        pygame.display.set_caption("snek 2d 0.1")
        self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.player = player.Player(self, 100, 0)
        self.objects = [gameObject.Object(self, 400, 0),
            gameObject.Object(self, 500, 100, 100,20),
            gameObject.Object(self, 600, 120, 100,20),
            gameObject.Object(self, 700, 140, 100,20),
            gameObject.Object(self, 800, 160, 100,20),
            gameObject.Object(self, 900, 180, 100,20),
            gameObject.Object(self, 1000, 200, 100,20),
            gameObject.Object(self, 1100, 220, 100,20),
            gameObject.Object(self, 1200, 240, 100,20),
            gameObject.Object(self, 800, 0),
            gameObject.Object(self, 1200, 10),
            gameObject.Object(self, 700, 500, 600, 40),
            gameObject.Object(self, 0, 0, 4, 720),
            gameObject.Object(self, 1260, 0, 4, 700),
            gameObject.Object(self, 0, 710, 1200, 4),
            gameObject.Object(self, 0, 0, 1200, 4)]
    def on_loop(self):
        """game logic here"""
        self.player.move(self.getInputMove())
    def on_render(self):
        """render stuff here"""
        self.display_surface.fill((30,20,10))        
        for obj in self.objects:
            obj.render()
        self.player.render()
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
