import math
from game_settings import *
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window
from kivy import platform

#######################
## Controls handling ##
#######################
# WASD to move
# Joystick GUI to be implemented in future for mobile

class Controls(FloatLayout):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)

        self.player = player
        
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)

    def keyboard_closed(self):
        self.keyboard_unbind(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if keycode[1] == 'w':
            self.player.dir[1] = 1
            

        if keycode [1] == 's':
            self.player.dir[1] = -1
            

        if keycode[1] == 'a':
            self.player.dir[0] = -1
            

        if keycode[1] == 'd':
            self.player.dir[0] = 1          

        return True
    
    def on_keyboard_up(self, keyboard, keycode, *args):
        if keycode[1] == 'w':
            self.player.dir[1] = 0
            

        if keycode [1] == 's':
            self.player.dir[1] = 0
            

        if keycode[1] == 'a':
            self.player.dir[0] = 0
            

        if keycode[1] == 'd':
            self.player.dir[0] = 0
            

        return True
