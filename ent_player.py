from ent_ship import *

from kivy.uix.image import Image
from game_controls import *
from utilities import *

######################################
##      Player object handling      ## 
## Handles controls and player data ##
######################################

class Player(Ship):
    def __init__(self, enemies, inactive_bullets, active_bullets, **kwargs):
        super().__init__(**kwargs)

        ## Bullet group references ##
        self.inactive_bullets = inactive_bullets
        self.active_bullets = active_bullets

        self.size_hint = (.1, .1)

        ## Sprite handling ##
        self.image = Image()
        self.image.source = "Graphics/Player/1/Idle/Ship_LVL_1.png"
        self.image.allow_stretch = True
        self.add_widget(self.image)
        self.image.size_hint = (None, None)
        self.image.size = (dp(50), dp(50))
        
        ## Animation sprites data - Imports from utilities.py ##
        anim_states = {'Dead': [], 'Move': [], 'Idle': []}
        self.animations = get_animations(anim_states, 'Player', '1')

        ## Player Data ##
        self.state = "Idle"        

        ## Enemy targeting data ##
        self.enemies = enemies
        self.target = None

        ## Init functions ##
        self.init_controls()

    def on_size(self, *args):
        pass

    def init_pos(self, pos):

        ## Updates position when spawned -- Called from battle script ##

        half_width = self.width * 3
        half_height = self.height

        pos = (pos[0] - half_width, pos[1] - half_height)
        
        self.pos = pos
        print("Player init position ###############")

    def update(self, dt):
        self.move(dt)
        self.check_state()
        self.animate()
        self.aim(dt)
        self.fire()
        self.fire_cooldown(dt)

    def init_controls(self):

        ## Init control handling script ##

        controls = Controls(self)
        self.add_widget(controls)
        print("Init player controls ###################")

    