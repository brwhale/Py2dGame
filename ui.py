"""simple ui manager for a simple 2d python game"""
import pygame

class UI:
    """manager for all ui"""
    def __init__(self, appRef):
        self.appRef = appRef
        pygame.font.init()
        self.font = pygame.font.Font("font/FiraCode-Retina.ttf", 46)
        self.menu = MainMenu(appRef, self)
        self.characterMenu = CharacterMenu(appRef, self)
    def render(self):
        """render the ui"""
        health = self.appRef.player.health * 2.55
        if (health > 255):
            health = 255
        elif (health < 0):
            health = 0
        pygame.draw.rect(self.appRef.draw_surface,(255-health,health,0),(50,50,3 * health,50))

        if self.appRef.player.invWindowOpen:
            self.characterMenu.render(self.appRef.player)
        if self.appRef.paused:
            # draw pause menu
            self.menu.render()
    def update(self):
        self.menu.update(None, None)
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
    def __init__(self, message, position, size = (0,0), color = (0,0,0), triggerFunc = None, menuRef = None, bgColor = None, fontSize = None):
        self.message = message
        self.menuRef = menuRef
        self.color = color
        self.bgColor = bgColor
        self.triggerFunc = triggerFunc
        self.hovered = False
        self.counter = 0
        self.counterSpeed = .1
        self.clicked = False
        if fontSize is None:
            fontSize = size[1]
        self.fontSize = fontSize
        self.font = pygame.font.Font("font/FiraCode-Retina.ttf", fontSize)
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
                    if self.triggerFunc is not None:
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
        #self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+3)%4]), (self.position[0] + 3, self.position[1] + 3))
        #self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+2)%4]), (self.position[0] + 2, self.position[1] + 2))
        #self.menuRef.appRef.draw_surface.blit(self.menuRef.bigFont.render(self.message, True, cols[int(self.counter+1)%4]), (self.position[0] + 1, self.position[1] + 1))
        self.menuRef.appRef.draw_surface.blit(self.font.render(self.message, True, cols[int(self.counter)%4]), (self.position[0]+self.fontSize/9,self.position[1]-self.fontSize/9))

class UIView:
    """base class for menus and views, based on ios"""
    def __init__(self, appRef, ui, position, size, parent = None, bgColor = (200,190,160)):
        self.appRef = appRef
        self.bgColor = bgColor
        self.parent = parent
        self.ui = ui
        self.w, self.h = size
        self.x, self.y = position
        #background button to capture events
        self.controls = [Button("", position, size, (0,0,0), ui.triggerNone)]
        for cntrl in self.controls:
            cntrl.menuRef = self
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
            for control in reversed(self.controls):
                if control.update(mpos, mclick):
                    ret = True
                    break
        return ret

    def render(self):
        """render our view and then the controls and subviews"""
        pygame.draw.rect(self.appRef.draw_surface,self.bgColor,(self.x,self.y,self.w,self.h))
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

class CharacterMenu:
    def __init__(self, appRef, ui):
        self.appRef = appRef
        self.view = UIView(appRef, ui,(700,120),(900,860))
        self.view.addControl(Button("test character menu!",(100,100), fontSize = 30))

        self.portraitView = UIView(appRef, ui, (300,120),(380,340))
        self.portraitView.addControl(Button("picture here", (20,20), fontSize = 20))
        self.levelReadout = Button("", (20,290), fontSize = 20)
        self.experienceBar = Button("",(20, 310), (340, 10), bgColor = (0,100,30))
        self.experienceBarFill = Button("",(20, 310), (0, 10), bgColor = (0,200,30))
        self.portraitView.addControl(self.levelReadout)        
        self.portraitView.addControl(self.experienceBar)
        self.portraitView.addControl(self.experienceBarFill)    

        self.statsView = UIView(appRef, ui, (300,480),(380,500))
        statfontsize = 30
        yoffset = 80
        spacing = 60
        buttonsize = (340, statfontsize)
        self.spendLevelsMessage = Button("", (statfontsize,50),fontSize = 20, color = (200,160,43))
        self.statsCON = Button("", (statfontsize,yoffset), size = buttonsize, triggerFunc = self.addCON)
        self.statsSTR = Button("", (statfontsize,yoffset+spacing),size = buttonsize, triggerFunc = self.addSTR)
        self.statsDEX = Button("", (statfontsize,yoffset+spacing*2),size = buttonsize, triggerFunc = self.addDEX)
        self.statsINT = Button("", (statfontsize,yoffset+spacing*3),size = buttonsize, triggerFunc = self.addINT)
        self.statsWIS = Button("", (statfontsize,yoffset+spacing*4),size = buttonsize, triggerFunc = self.addWIS)
        self.statsPER = Button("", (statfontsize,yoffset+spacing*5),size = buttonsize, triggerFunc = self.addPER)
        self.statsView.addControl(self.spendLevelsMessage)
        self.statsView.addControl(self.statsCON)
        self.statsView.addControl(self.statsSTR)
        self.statsView.addControl(self.statsDEX)
        self.statsView.addControl(self.statsINT)
        self.statsView.addControl(self.statsWIS)
        self.statsView.addControl(self.statsPER)

        self.view.addSubView(self.statsView)
        self.view.addSubView(self.portraitView)
    
    def addCON(self):
        if self.appRef.player.unusedStatPoints > 0:
            self.appRef.player.unusedStatPoints -= 1
            self.appRef.player.constitution += 1

    def addSTR(self):
        if self.appRef.player.unusedStatPoints > 0:
            self.appRef.player.unusedStatPoints -= 1
            self.appRef.player.strength += 1

    def addDEX(self):
        if self.appRef.player.unusedStatPoints > 0:
            self.appRef.player.unusedStatPoints -= 1
            self.appRef.player.dexterity += 1

    def addINT(self):
        if self.appRef.player.unusedStatPoints > 0:
            self.appRef.player.unusedStatPoints -= 1
            self.appRef.player.intelligence += 1

    def addWIS(self):
        if self.appRef.player.unusedStatPoints > 0:
            self.appRef.player.unusedStatPoints -= 1
            self.appRef.player.wisdom += 1

    def addPER(self):
        if self.appRef.player.unusedStatPoints > 0:
            self.appRef.player.unusedStatPoints -= 1
            self.appRef.player.perception += 1

    def update(self):
        self.view.update(None, None)
    def render(self, player):
        self.levelReadout.message = "Human Cleric; Level: " + str(self.appRef.player.level)
        self.experienceBarFill.size = 340 * (self.appRef.player.experience / self.appRef.player.experienceToLevel), self.experienceBarFill.size[1]
        
        addPointButtonText = ""
        if self.appRef.player.unusedStatPoints > 0:
            self.spendLevelsMessage.message = str(self.appRef.player.unusedStatPoints) + " unused stat points"
            addPointButtonText = " +"
        else:
            self.spendLevelsMessage.message = ""
        self.statsCON.message = "Constitution: " + str(self.appRef.player.constitution) + addPointButtonText
        self.statsSTR.message = "Strength:     " + str(self.appRef.player.strength) + addPointButtonText
        self.statsDEX.message = "Dexterity:    " + str(self.appRef.player.dexterity) + addPointButtonText
        self.statsINT.message = "Intelligence: " + str(self.appRef.player.intelligence) + addPointButtonText
        self.statsWIS.message = "Wisdom:       " + str(self.appRef.player.wisdom) + addPointButtonText
        self.statsPER.message = "Perception:   " + str(self.appRef.player.perception) + addPointButtonText
        self.view.render()

class MainMenu(Menu):
    """simple main menu"""
    def __init__(self, appRef, ui):
        Menu.__init__(self, appRef, ui, (900, 800))
        self.messages = [("Continue", ui.triggerContinue), ("Settings", self.triggerSettings), ("Quit", ui.triggerQuit)]
        padd = 106
        yoff = padd
        paddx = padd
        for message in self.messages:
            self.controls.append(Button(message[0], (paddx, yoff), (600,padd), (255,220,212), message[1], menuRef = self, bgColor = (60,60,60)))
            yoff += padd + 30

    def triggerSettings(self):
        """show settings"""
        self.view = UIView(self.appRef, self.ui, (500, 100), (400, 800), parent = self)
        self.view.addControl(Button("test1T1IL|^*gqQ~`", (20, 200), (1000, 100), (123,123,200), self.ui.triggerNone, bgColor = (0,0,0)))
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
