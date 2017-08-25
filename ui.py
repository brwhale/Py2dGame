"""simple ui manager for a simple 2d python game"""
import pygame

class UI:
    """manager for all ui"""
    def __init__(self, appRef):
        self.appRef = appRef
        pygame.font.init()
        self.font = pygame.font.Font("font/FiraCode-Retina.ttf", 46)
        self.menu = MainMenu(appRef, self)
    def render(self):
        """render the ui"""
        health = self.appRef.player.health * 2.55
        if (health > 255):
            health = 255
        elif (health < 0):
            health = 0
        pygame.draw.rect(self.appRef.draw_surface,(255-health,health,0),(50,50,3 * health,50))
        if self.appRef.paused:
            # draw pause menu
            self.menu.render()
    # basic button triggers that will be shared by a lot of controls
    def triggerNone(self):
        print("clicked something")
    def triggerMsg(self):
        print("clicked test2")
    def triggerQuit(self):
        self.appRef.on_exit()
    def triggerContinue(self):
        self.appRef.paused = False
        self.menu = MainMenu(self.appRef, self)

class Control:
    """basic parent class for all ui controls, buttons, sliders, whatever"""
    def __init__(self, position, size, menuRef):
        self.size = size
        if menuRef is not None:
            self.position = position[0] + menuRef.x, position[1] + menuRef.y        
            self.menuRef = menuRef
        else:
            self.position = position[0], position[1]  

class Button(Control):
    """button class derived from control"""
    def __init__(self, message, position, size, color, triggerFunc, menuRef = None, bgColor = None):
        self.message = message
        self.menuRef = menuRef
        self.color = color
        self.bgColor = bgColor
        self.triggerFunc = triggerFunc
        self.hovered = False
        self.counter = 0
        self.counterSpeed = .1
        self.clicked = False
        Control.__init__(self, position, size, menuRef)

    def update(self, mposition, mclicked):
        """handle hover, mouse clicks, whatever"""
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
            return True
        else:
            self.hovered = False
            self.counter = False
        if not mclicked:
            self.clicked = False
        return False

    def render(self):
        """draw the button to the screen"""
        #draw bg if set
        if self.bgColor is not None:
            pygame.draw.rect(self.menuRef.appRef.draw_surface,self.bgColor,(self.position[0],self.position[1],self.size[0],self.size[1]))
        
        midbcol = self.color[0]*0.4, self.color[1]*0.4, self.color[2]*0.4
        midcol = self.color[0]*0.6, self.color[1]*0.6, self.color[2]*0.6
        midfcol = self.color[0]*0.8, self.color[1]*0.8, self.color[2]*0.8
        cols = [self.color, midfcol, midcol, midbcol]
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+3)%4]), (self.position[0] + 3, self.position[1] + 3))
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+2)%4]), (self.position[0] + 2, self.position[1] + 2))
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+1)%4]), (self.position[0] + 1, self.position[1] + 1))
        self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter)%4]), self.position)

class UIView:
    """base class for menus and views, based on ios"""
    def __init__(self, appRef, ui, position, size, fontSize = 106, parent = None):
        self.appRef = appRef
        self.parent = parent
        self.ui = ui
        self.fontSize = fontSize
        self.bigFont = pygame.font.Font("font/FiraCode-Retina.ttf", fontSize)
        self.controls = []
        for cntrl in self.controls:
            cntrl.menuRef = self
        self.w, self.h = size
        self.x, self.y = position
        self.subViews = []

    def removeFromParent(self):
        self.parent.subViews.remove(self)

    def addSubView(self, sub):
        """add a sub view to the stack"""
        self.subViews.append(sub)

    def addControl(self, control):
        """add a control to the stack"""
        if control.menuRef is None:
            control.menuRef = self
            control.position = control.position[0] + self.x, control.position[1] + self.y
        self.controls.append(control)
    
    def update(self, mpos, mclick):
        """dispatch updates to child objects"""
        ret = False
        if (mpos is None and mclick is None):
            mpos = pygame.mouse.get_pos()
            mpos = mpos[0] * self.appRef.drawSize[0] / self.appRef.size[0], mpos[1] * self.appRef.drawSize[1] / self.appRef.size[1]
            mclick = pygame.mouse.get_pressed()[0]
        for sub in self.subViews:
            if sub.update(mpos, mclick):
                ret = True
                break
        if not ret:
            for control in self.controls:
                if control.update(mpos, mclick):
                    ret = True
                    break
        return ret

    def render(self):
        """render our view and then the controls and subviews"""
        pygame.draw.rect(self.appRef.draw_surface,(200,190,160),(self.x,self.y,self.w,self.h))
        for control in self.controls:
            control.render()
        for sub in self.subViews:
            sub.render()

class Menu(UIView):
    """basic menu based on view"""
    def __init__(self, appRef, ui, size):
        UIView.__init__(self, appRef, ui, (0,0), (0,0))
        self.w, self.h = size
        self.x, self.y = (self.appRef.drawSize[0]-self.w)/2, (self.appRef.drawSize[1]-self.h)/2

class MainMenu(Menu):
    """simple main menu"""
    def __init__(self, appRef, ui):
        Menu.__init__(self, appRef, ui, (900, 800))
        self.messages = [("continue", ui.triggerContinue), ("settings", self.triggerSettings), ("quit", ui.triggerQuit)]
        padd = self.fontSize
        yoff = padd
        paddx = padd
        for message in self.messages:
            self.controls.append(Button(message[0], (paddx, yoff), (600,padd), (255,220,212), message[1], menuRef = self, bgColor = (60,60,60)))
            yoff += padd + 30

    def triggerSettings(self):
        """show settings"""
        self.view = UIView(self.appRef, self.ui, (500, 100), (400, 800), parent = self)
        self.view.addControl(Button("test1", (20, 200), (200, 100), (123,123,200), self.ui.triggerNone, bgColor = (0,0,0)))
        self.view.addControl(Button("test3", (20, 400), (200, 100), (123,123,200), self.triggerSettings2, bgColor = (0,0,0)))
        self.view.addControl(Button("back", (20, 600), (300, 100), (123,123,200), self.view.removeFromParent, bgColor = (0,0,0)))
        self.addSubView(self.view)

    def triggerSettings2(self):
        """show settings"""
        view = UIView(self.appRef, self.ui, (self.view.x + 20, 100), (400, 800), parent = self.view)
        view.addControl(Button("test2", (20, 200), (200, 100), (123,123,200), self.ui.triggerMsg, bgColor = (0,0,0)))
        view.addControl(Button("test4", (20, 400), (200, 100), (123,123,200), self.triggerSettings2, bgColor = (0,0,0)))
        view.addControl(Button("back", (20, 600), (300, 100), (123,123,200), view.removeFromParent, bgColor = (0,0,0)))
        self.view.addSubView(view)
        self.view = view
