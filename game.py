"""Simple 2d game thing in python"""
import pygame
import jsonpickle
# pylint: disable=W0614
# pylint: disable=W0401
from pygame.locals import *
import events
import player
import gameLevels
import gameObject
import movingPlatform
import ui

class App(events.CEvent):
    """main class for game"""
    # pylint: disable=E1101
    def __init__(self):
        """window init"""
        self._running = True
        self.display_surface = None
        self.draw_surface = None
        self.size = None, None
        self.oldSize = None, None
        self.screenSize = None, None
        self.printFPS = False
        self.paused = False
        self.ui = None
        self.drawSize = 1920, 1080
        self.inverseAspectRatio = self.drawSize[1] / self.drawSize[0]
        self.padding = None
        self.fpsUpdateCounter = 0
        self.offset = 0, 0
        self.levels = gameLevels.Levels(self)
        self.saveLevels = False
        self.clock = None
        self.fullscreen = False
        events.CEvent.__init__(self, self)

    def on_init(self):
        """game init"""
        # pylint: disable=E1121
        # pylint: disable=W0201
        pygame.init()
        pygame.display.set_caption("snek 2d 0.1")
        info = pygame.display.Info()
        self.screenSize = (info.current_w, info.current_h)
        self.draw_surface = pygame.Surface(self.drawSize)
        self.resize(1280, 720)
        self._running = True
        self.clock = pygame.time.Clock()
        self.ui = ui.UI(self)
        self.player = player.Player(self, 100, 20)
        self.loadMap("levels/level1.json")
        
    def loadMap(self, mapFile):
        try:
            with open(mapFile, 'r') as savefile:
                self.objects = jsonpickle.decode(savefile.read())
                for obj in self.objects:
                    obj.init(self)
        except:
            self.objects = self.levels.level2()
            if self.saveLevels:
                with open(mapFile, 'w') as outfile:    
                    outfile.write(jsonpickle.encode(self.objects))
            for obj in self.objects:
                obj.init(self)

    def on_loop(self):
        """game logic here"""
        if not self.paused:
            self.player.move(self.getInputMove())
            self.player.update()
            # update screen offset
            boundMinX = self.offset[0] + self.padding*2
            boundMaxX = self.offset[0] + self.drawSize[0] - self.padding*2 - self.player.size[0]
            boundMinY = self.offset[1] + self.padding
            boundMaxY = self.offset[1] + self.drawSize[1] - self.padding - self.player.size[1]
            if (self.player.position[0] < boundMinX):
                self.offset = self.offset[0] + (self.player.position[0] - boundMinX), self.offset[1]
            elif (self.player.position[0] > boundMaxX):
                self.offset = self.offset[0] + (self.player.position[0] - boundMaxX), self.offset[1]
            if (self.player.position[1] < boundMinY):
                self.offset = self.offset[0], self.offset[1] + (self.player.position[1] - boundMinY)
            elif (self.player.position[1] > boundMaxY):
                self.offset = self.offset[0], self.offset[1] + (self.player.position[1] - boundMaxY)
            for obj in self.objects:
                obj.update()
        else:
            self.ui.update()
        if self.player.invWindowOpen:
            self.ui.characterMenu.update()

    def keyboardTestFunction(self):
        self.player.experience += 9

    def on_resize(self,event):
        self.resize(event.w, event.h)

    def resize(self, x, y):
        """resize the window"""
        if not self.fullscreen:
            self.size = x, int(x * self.inverseAspectRatio)
            self.padding = (self.size[0] + self.size[1])/14.0
            self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)        

    def toggleFullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
            self.resize(self.oldSize[0], self.oldSize[1])            
        else:
            self.fullscreen = True
            self.oldSize = self.size
            self.size = self.screenSize
            self.padding = (self.size[0] + self.size[1])/14.0
            self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)

    def reset(self):
        """reset the player"""
        self.offset = 0, 0
        self.player.reset()
        self.loadMap("levels/level1.json")

    def on_render(self):
        """render stuff here"""
        self.draw_surface.fill((20,20,20))        
        for obj in self.objects:
            obj.render()
        self.player.render()
        # ui
        self.ui.render()

        pygame.transform.scale(self.draw_surface.convert_alpha(), self.size, self.display_surface)
        pygame.display.flip()
        self.clock.tick_busy_loop(60)
        if self.printFPS:
            if self.fpsUpdateCounter < 30:
                self.fpsUpdateCounter += 1
            else:
                self.fpsUpdateCounter = 0
                print(self.clock.get_fps())

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
