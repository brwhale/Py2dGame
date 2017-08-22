"""Simple 2d game thing in python"""
import pygame
# pylint: disable=W0614
# pylint: disable=W0401
from pygame.locals import *
import events
import player
import gameLevels

class App(events.CEvent):
    """main class for game"""
    def __init__(self):
        """window init"""
        self._running = True
        self.display_surface = None
        self.size = self.weight, self.height = None, None
        self.padding = None
        self.offset = 0, 0
        self.levels = gameLevels.Levels(self)
        self.clock = None
        events.CEvent.__init__(self, self)
    def on_init(self):
        """game init"""
        # pylint: disable=E1101
        # pylint: disable=W0201
        pygame.init()
        pygame.display.set_caption("snek 2d 0.1")
        self.resize(1280, 720)
        self._running = True
        self.clock = pygame.time.Clock()
        self.player = player.Player(self, 100, 20)
        self.objects = self.levels.level1()
    def on_loop(self):
        """game logic here"""
        self.player.move(self.getInputMove())
    def on_resize(self,event):
        self.resize(event.w, event.h)
    def resize(self, x, y):
        # pylint: disable=E1101
        self.size = self.weight, self.height = x, y
        self.padding = (self.size[0] + self.size[1])/14.0
        self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    def reset(self):
        self.player.reset()
    def on_render(self):
        """render stuff here"""
        self.display_surface.fill((30,20,10))        
        for obj in self.objects:
            obj.render()
        self.player.render()
        pygame.display.flip()
        self.clock.tick_busy_loop(60)
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
