import gameObject
import movingPlatform

class Levels:
    def __init__(self, appRef):
        self.appRef = appRef

    def level1(self):
        return [movingPlatform.MovingPlatform(self.appRef, 400, 0, vertical = True),
            gameObject.Object(self.appRef, 500, 100, 100,20),
            gameObject.Object(self.appRef, 600, 120, 100,20),
            gameObject.Object(self.appRef, 700, 140, 100,20),
            gameObject.Object(self.appRef, 800, 160, 100,20),
            gameObject.Object(self.appRef, 900, 180, 100,20),
            gameObject.Object(self.appRef, 1000, 200, 100,20),
            gameObject.Object(self.appRef, 1100, 220, 100,20),
            gameObject.Object(self.appRef, 1200, 240, 100,20),
            gameObject.Object(self.appRef, 1300, 260, 100,20),
            gameObject.Object(self.appRef, 1400, 280, 100,20),
            gameObject.Object(self.appRef, 1500, 300, 100,20),
            gameObject.Object(self.appRef, 1600, 320, 100,20),
            gameObject.Object(self.appRef, 1700, 340, 100,20),
            gameObject.Object(self.appRef, 1800, 360, 100,20),
            gameObject.Object(self.appRef, 1900, 380, 100,20),
            gameObject.Object(self.appRef, 2000, 400, 100,20),
            gameObject.Object(self.appRef, 2100, 420, 100,20),
            gameObject.Object(self.appRef, 2200, 440, 100,20),
            gameObject.Object(self.appRef, 2300, 460, 100,20),
            gameObject.Object(self.appRef, 2400, 480, 100,20),            
            gameObject.Object(self.appRef, 3300, 300, 100,20),
            gameObject.Object(self.appRef, 3200, 320, 100,20),
            gameObject.Object(self.appRef, 3100, 340, 100,20),
            gameObject.Object(self.appRef, 3000, 360, 100,20),
            gameObject.Object(self.appRef, 2900, 380, 100,20),
            gameObject.Object(self.appRef, 2800, 400, 100,20),
            gameObject.Object(self.appRef, 2700, 420, 100,20),
            gameObject.Object(self.appRef, 2600, 440, 100,20),
            gameObject.Object(self.appRef, 2500, 460, 100,20),
            movingPlatform.MovingPlatform(self.appRef, 800, 0),
            gameObject.Object(self.appRef, 1200, -30),
            gameObject.Object(self.appRef, 700, 500, 600, 40),
            gameObject.Object(self.appRef, 0, 0, 4, 720),
            gameObject.Object(self.appRef, 11260, 0, 4, 700),
            gameObject.Object(self.appRef, 0, 710, 1200, 4),
            gameObject.Object(self.appRef, 0, -20, 11200, 24),
            gameObject.Object(self.appRef, 0, -110, 1200, 4)]
