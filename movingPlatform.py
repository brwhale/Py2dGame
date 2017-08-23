import gameObject

class MovingPlatform(gameObject.Object):
    def __init__(self, x = 0, y = 0, xsize = 100, ysize = 100, vertical = False, maxDistance = 500, speed = 1):
        self.distance = 0
        self.maxDistance = maxDistance
        self.reverse = False
        self.speed = speed
        self.vertical = vertical
        gameObject.Object.__init__(self, x, y, xsize, ysize)

    def update(self):
        if self.reverse:
            addAmt = -self.speed
        else:
            addAmt = self.speed
        self.distance += addAmt

        if self.vertical:
            self.position = self.position[0], self.position[1] + addAmt
            self.velocity = self.velocity[0], addAmt
        else:
            self.position = self.position[0] + addAmt, self.position[1]
            self.velocity = addAmt, self.velocity[1]

        if self.distance < 0 or self.distance > self.maxDistance:
            self.reverse = not self.reverse