import player

class NPC(player.Player):
    def __init__(self, x = 0, y = 0, w = 40, h = 40, contactDamage = 20, active = True):
        player.Player.__init__(self,None,x,y,w,h)
        self.oldPosition = self.position
        self.goingRight = True
        self.triedJumping = False
        self.contactDamage = contactDamage
        self.player = False
        self.sentient = True
        self.active = active
        self.turnAroundCount = 0

    def init(self, appRef):
        self.appRef = appRef

    def update(self):
        x,y = 0,0
        if not self.active:
            self.move((x,y))
            return
        self.turnAroundCount -= 1
        if self.turnAroundCount <= 0:
            self.goingRight = self.appRef.player.position[0] > self.position[0]
            self.turnAroundCount = 40
        x = 0.1 if self.goingRight else -0.1
        self.oldPosition = self.position 
        self.move((x,y))
        if self.oldPosition[0] == self.position[0] and self.turnAroundCount <= 0:
            self.goingRight = not self.goingRight
            self.turnAroundCount = 40
