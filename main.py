from kivy.config import Config
from game_settings import *
Config.set('graphics', 'width', str(WIDTH))
Config.set('graphics', 'height', str(HEIGHT))
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'maxfps', str(FPS))

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

import cProfile

from battle import *

##########################################
##        Main Project Set-up           ##
## Handles different scenes within game ##
## IE: Main menu, upgrade menu, battle  ##
##########################################

class Game(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.game_state = "battle"
        self.game_screen = None

        self.update_screen()

    def update_screen(self):
        if self.game_state == "battle":
            self.init_battle()

    def init_battle(self):
        self.game_screen = Battle()
        self.add_widget(self.game_screen)

    

class HordeShmupApp(App):
    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def build(self):
        return Game()
    
    def on_stop(self):
        self.profile.disable()
        self.profile.print_stats()
    
HordeShmupApp().run()