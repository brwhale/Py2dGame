import gameObject
import movingPlatform

class Levels:
    def __init__(self, appRef):
        self.appRef = appRef

    def level1(self):
        return [movingPlatform.MovingPlatform(400, 0, vertical = True),
            movingPlatform.MovingPlatform(400, 400, 500, 20, vertical = False),
            gameObject.Object(600, 120, 100,20),
            gameObject.Object(700, 140, 100,20),
            gameObject.Object(800, 160, 100,20),
            gameObject.Object(900, 180, 100,20),
            gameObject.Object(1000, 200, 100,20),
            gameObject.Object(1100, 220, 100,20),
            gameObject.Object(1200, 240, 100,20),
            gameObject.Object(1300, 260, 100,20),
            gameObject.Object(1400, 280, 100,20),
            gameObject.Object(1500, 300, 100,20),
            gameObject.Object(1600, 320, 100,20),
            gameObject.Object(1700, 340, 100,20),
            gameObject.Object(1800, 360, 100,20),
            gameObject.Object(1900, 380, 100,20),
            gameObject.Object(2000, 400, 100,20),
            gameObject.Object(2100, 420, 100,20),
            gameObject.Object(2200, 440, 100,20),
            gameObject.Object(2300, 460, 100,20),
            gameObject.Object(2400, 480, 100,20),            
            gameObject.Object(3300, 300, 100,20),
            gameObject.Object(3200, 320, 100,20),
            gameObject.Object(3100, 340, 100,20),
            gameObject.Object(3000, 360, 100,20),
            gameObject.Object(2900, 380, 100,20),
            gameObject.Object(2800, 400, 100,20),
            gameObject.Object(2700, 420, 100,20),
            gameObject.Object(2600, 440, 100,20),
            gameObject.Object(2500, 460, 100,20),
            movingPlatform.MovingPlatform(400, 0, maxDistance = 2000, speed = 50),
            gameObject.Object(1200, -30),
            movingPlatform.MovingPlatform(700, 420, 60, 140, vertical = True, maxDistance = 200, speed = 3),
            gameObject.Object(0, 0, 4, 720),
            gameObject.Object(11260, 0, 4, 700),
            gameObject.Object(0, 710, 1200, 4),
            gameObject.Object(0, -20, 11200, 24),
            gameObject.Object(0, -110, 1200, 4)]
