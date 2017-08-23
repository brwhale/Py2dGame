import gameObject

class MovingPlatform(gameObject.Object):
    def __init__(self, appRef, x = 0, y = 0, xsize = 100, ysize = 100, vertical = False):
        self.distance = 0
        self.maxDistance = 500
        self.reverse = False
        self.vertical = vertical
        gameObject.Object.__init__(self, appRef, x, y, xsize, ysize)
        
    def update(self):
        addAmt = 1
        if self.reverse:
            addAmt = -1
        self.distance += addAmt

        if self.vertical:
            self.position = self.position[0], self.position[1] + addAmt
            self.velocity = self.velocity[0], addAmt
        else:
            self.position = self.position[0] + addAmt, self.position[1]
            self.velocity = addAmt, self.velocity[1]

        if self.distance < 0 or self.distance > self.maxDistance:
            self.reverse = not self.reverse