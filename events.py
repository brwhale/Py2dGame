import pygame
from pygame.locals import *

class CEvent:
    upkey = 273
    downkey = 274
    rightkey = 275
    leftkey = 276
    wkey = 119
    akey = 97
    skey = 115
    dkey = 100
    rkey = 114
    up = False
    down = False
    right = False
    left = False
    r = False
    def getInputMove(self):
        x = 0
        y = 0
        if CEvent.up:
            y += 1
        if CEvent.down:
            y -= 1
        if CEvent.right:
            x += 1
        if CEvent.left:
            x -= 1
        return (x, y)
    def __init__(self, appRef):
        self.appRef = appRef
    def on_input_focus(self):
        pass
    def on_input_blur(self):
        pass
    def on_key_down_up(self, event, isdown):
        if event.key == CEvent.upkey or event.key == CEvent.wkey:
            CEvent.up = isdown
        elif event.key == CEvent.downkey or event.key == CEvent.skey:
            CEvent.down = isdown
        elif event.key == CEvent.rightkey or event.key == CEvent.dkey:
            CEvent.right = isdown
        elif event.key == CEvent.leftkey or event.key == CEvent.akey:
            CEvent.left = isdown
        elif event.key == CEvent.rkey:
            if isdown:
                if not CEvent.r:
                    self.appRef.reset()
            CEvent.r = isdown
    def on_mouse_focus(self):
        pass
    def on_mouse_blur(self):
        pass
    def on_mouse_move(self, event):
        pass
    def on_mouse_wheel(self, event):
        pass
    def on_lbutton_up(self, event):
        pass
    def on_lbutton_down(self, event):
        pass
    def on_rbutton_up(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_mbutton_up(self, event):
        pass
    def on_mbutton_down(self, event):
        pass
    def on_minimize(self):
        pass
    def on_restore(self):
        pass
    def on_resize(self,event):
        pass
    def on_expose(self):
        pass
    def on_exit(self):
        pass
    def on_user(self,event):
        pass
    def on_joy_axis(self,event):
        pass
    def on_joybutton_up(self,event):
        pass
    def on_joybutton_down(self,event):
        pass
    def on_joy_hat(self,event):
        pass
    def on_joy_ball(self,event):
        pass
    def on_event(self, event):
        if event.type == QUIT:
            self.on_exit()
 
        elif event.type >= USEREVENT:
            self.on_user(event)
 
        elif event.type == VIDEOEXPOSE:
            self.on_expose()
 
        elif event.type == VIDEORESIZE:
            self.on_resize(event)
 
        elif event.type == KEYUP:
            self.on_key_down_up(event, False)
 
        elif event.type == KEYDOWN:
            self.on_key_down_up(event, True)
 
        elif event.type == MOUSEMOTION:
            self.on_mouse_move(event)
 
        elif event.type == MOUSEBUTTONUP:
            if event.button == 0:
                self.on_lbutton_up(event)
            elif event.button == 1:
                self.on_mbutton_up(event)
            elif event.button == 2:
                self.on_rbutton_up(event)
 
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 0:
                self.on_lbutton_down(event)
            elif event.button == 1:
                self.on_mbutton_down(event)
            elif event.button == 2:
                self.on_rbutton_down(event)
 
        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()
 
if __name__ == "__main__" :
    event = CEvent()
