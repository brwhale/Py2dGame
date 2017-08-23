import pygame

class UI:
    def __init__(self, appRef):
        self.appRef = appRef
        pygame.font.init()
        self.font = pygame.font.Font("font/FiraCode-Retina.ttf", 46)
        self.menu = [MainMenu(appRef, self)]
    def render(self):
        health = self.appRef.player.health * 2.55
        if (health > 255):
            health = 255
        elif (health < 0):
            health = 0
        pygame.draw.rect(self.appRef.draw_surface,(255-health,health,0),(50,50,3 * health,50))
        if self.appRef.paused:
            # draw pause menu
            self.menu[-1].render()

class Control:
    def __init__(self, position, size):
        self.position = position
        self.size = size

class Button(Control):
    def __init__(self, menuRef, message, position, size, color, triggerFunc):
        self.message = message
        self.menuRef = menuRef
        self.color = color
        self.triggerFunc = triggerFunc
        self.hovered = False
        self.counter = 0
        self.counterSpeed = .1
        self.clicked = False
        Control.__init__(self, position, size)

    def update(self, mposition, mclicked):
        if mposition[0] > self.position[0] and mposition[0] < self.position[0] + self.size[0] and mposition[1] > self.position[1] and mposition[1] < self.position[1] + self.size[1]:
            if self.hovered:                
                if self.counter >= 3.5 or self.counter <= -0.5:
                    self.counterSpeed = -self.counterSpeed
                self.counter += self.counterSpeed
                if mclicked:
                    self.clicked = True
                elif self.clicked:
                    self.clicked = False
                    # trigger clickDownUpInside event
                    self.triggerFunc()
            self.hovered = True
        else:
            self.hovered = False
            self.counter = False
        if not mclicked:
            self.clicked = False

    def render(self):
        midbcol = self.color[0]*0.4, self.color[1]*0.4, self.color[2]*0.4
        midcol = self.color[0]*0.6, self.color[1]*0.6, self.color[2]*0.6
        midfcol = self.color[0]*0.8, self.color[1]*0.8, self.color[2]*0.8
        cols = [self.color, midfcol, midcol, midbcol]
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+3)%4]), (self.position[0] + 3, self.position[1] + 3))
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+2)%4]), (self.position[0] + 2, self.position[1] + 2))
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+1)%4]), (self.position[0] + 1, self.position[1] + 1))
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter)%4]), self.position)

class Menu:
    def __init__(self, appRef, ui, size):
        self.appRef = appRef
        self.ui = ui
        self.bigFont = pygame.font.Font("font/FiraCode-Retina.ttf", 106)
        self.controls = []
        self.w, self.h = size
        self.x, self.y = (self.appRef.drawSize[0]-self.w)/2, (self.appRef.drawSize[1]-self.h)/2

    def triggerNone(self):
        print("clicked something")
    
    def update(self):
        mpos = pygame.mouse.get_pos()
        mpos = mpos[0] * self.appRef.drawSize[0] / self.appRef.size[0], mpos[1] * self.appRef.drawSize[1] / self.appRef.size[1]
        mclick = pygame.mouse.get_pressed()[0]
        for control in self.controls:
            control.update(mpos, mclick)

    def render(self):
        pygame.draw.rect(self.appRef.draw_surface,(200,190,160),(self.x,self.y,self.w,self.h))
        for control in self.controls:
            control.render()

class MainMenu(Menu):
    def __init__(self, appRef, ui):
        Menu.__init__(self, appRef, ui, (900, 800))
        self.messages = [("continue", self.triggerContinue), ("settings", self.triggerSettings), ("quit", self.triggerQuit)]

        padd = 150
        yoff = padd
        paddx = padd + self.x
        for message in self.messages:
            self.controls.append(Button(self, message[0], (paddx, self.y + yoff), (600,padd), (255,220,212), message[1]))
            yoff += padd

    def triggerSettings(self):
        self.ui.menu.append(SettingsMenu(self.appRef,self.ui))

    def triggerQuit(self):
        self.appRef.on_exit()

    def triggerContinue(self):
        self.appRef.paused = False

class SettingsMenu(Menu):
    def __init__(self, appRef, ui):
        Menu.__init__(self, appRef, ui, (900, 800))
        self.messages = [("back", self.triggerBack), ("fullscreen", self.triggerNone), ("mute", self.triggerNone)]
        padd = 150
        yoff = padd
        paddx = padd + self.x
        for message in self.messages:
            self.controls.append(Button(self, message[0], (paddx, self.y + yoff), (600,padd), (255,220,212), message[1]))
            yoff += padd
            
    def triggerBack(self):
        del self.ui.menu[-1]
