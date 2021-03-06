"""player controls and stuff"""
import pygame

class Player:
    """see top"""
    def __init__(self, appRef, x = 0, y = 0, w = 60, h = 100):
        self.appRef = appRef
        self.size = w, h
        self.jumpSpeed = 24.1
        self.runSpeed = 0.7
        self.velocity = 0, 0
        self.kneeRatio = 0.25
        self.health = 100
        self.player = True
        self.position = x, y
        self.originalPosition = x, y
        self.sprite = pygame.image.load("tex/glider.jpg").convert()
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.onGround = False
        self.inventory = []
        self.invWindowOpen = False
        self.renderMode = 0
        self.level = 1
        self.experience = 0
        self.experienceToLevel = 100
        self.experienceTotal = 0
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.perception = 10
        self.unusedStatPoints = 0

    def reset(self):
        self.position = self.originalPosition
        self.velocity = 0, 0
        self.health = 100

    def testPoint(self, pos):
        for obj in self.appRef.objects:
            x1 = obj.position[0]
            x2 = obj.position[0] + obj.size[0] 
            y1 = obj.position[1]
            y2 = obj.position[1] + obj.size[1]
            if pos[0] > x1 and pos[0] < x2:
                if pos[1] > y1 and pos[1] < y2:
                    return True
        return False

    def move(self, pos):
        # transform input move vector into character move vector
        x, y = pos[0] * self.runSpeed, 0 if pos[1] < 0 else pos[1] * self.jumpSpeed
        if pos[1] < 0:
            self.appRef.offset = self.appRef.offset[0], self.appRef.offset[1] + pos[1]
        # add gravity
        if not self.onGround:
            self.velocity = self.velocity[0], self.velocity[1] - 0.98
            # mid air controls
            x = x * self.runSpeed
            y = 0
        # calculate new position from velocity
        x += self.velocity[0]
        y += self.velocity[1]
        self.velocity = x, y
        newpos = (x + self.position[0], y + self.position[1])
        # calculate colisions from new position
        self.onGround = False
        for obj in self.appRef.objects:
            if obj == self:
                break
            # get boundries
            x1 = obj.position[0] - self.size[0]
            x2 = obj.position[0] + obj.size[0] 
            y1 = obj.position[1] - self.size[1]
            y2 = obj.position[1] + obj.size[1]
            if newpos[0] > x1 and newpos[0] < x2:
                if newpos[1] > y1 and newpos[1] < y2:
                    # collsion
                    # modify health if needed (negative damage heals you)
                    if (self.player):
                        self.health -= obj.contactDamage
                    # get collision direction
                    xx = ((self.position[0] - x1) + (self.position[0] - x2)) / (self.size[0] + obj.size[0])
                    absx = abs(xx)
                    yy = ((self.position[1] - y1) + (self.position[1] - y2)) / (self.size[1] + obj.size[1])
                    absy = abs(yy)
                    if (absx > absy):
                        # hit from side, check for stair climb
                        # foot position
                        testpos = newpos[0], newpos[1] + 1                        
                        if xx < 0:
                            # right side
                            testpos = testpos[0] + self.size[0] + 1, testpos[1]
                            blockEdge = obj.position[0] - self.size[0]
                        else:
                            # left side
                            testpos = testpos[0] - 1, testpos[1]
                            blockEdge = obj.position[0] + obj.size[0]
                        # knee positon
                        testpos2 = testpos[0], testpos[1] + self.size[1]*self.kneeRatio
                        if self.testPoint(testpos) and not self.testPoint(testpos2):
                            # climbing!
                            newpos = newpos[0], self.position[1] + (y2 - self.position[1])*self.kneeRatio
                        else:
                            # too high! we are gonna smack it
                            # take object's x velocity so it can push us, only if it's moving towards us
                            if obj.position[0] > self.position[0] == obj.velocity[0] < 0:
                                newpos = blockEdge + obj.velocity[0], newpos[1]
                            else:
                                newpos = blockEdge, newpos[1]
                    else:
                        # hit from top or bottom                     
                        if yy >= 0:
                            # landed on something
                            self.velocity = self.velocity[0] * 0.9 + obj.velocity[0] * 0.1, 0
                            newpos = newpos[0], y2
                            self.onGround = True
                        else:
                            # bumped head
                            newpos = newpos[0], self.position[1]
                            if self.velocity[1] > 0:
                                self.velocity = self.velocity[0], 0
        # update position taking everyhting into account
        self.position = newpos
    def update(self):
        # we might have taken enough collision damage to die, better check
        if self.health < 0:
            self.appRef.reset()
            return
        if self.experience >= self.experienceToLevel:
            self.experienceTotal += self.experienceToLevel
            self.experience -= self.experienceToLevel
            self.experienceToLevel *= 1.6
            self.level += 1
            self.unusedStatPoints += 1

    def render(self):
        x, y = self.position
        self.appRef.draw_surface.blit(self.sprite, (x - self.appRef.offset[0], (self.appRef.drawSize[1] - self.size[1])-(y - self.appRef.offset[1])), None, self.renderMode)
