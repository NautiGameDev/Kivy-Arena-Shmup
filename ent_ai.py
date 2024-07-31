from ent_ship import *

from kivy.metrics import dp
from kivy.uix.image import Image
from utilities import *

class AI(Ship):
    def __init__(self, pos, enemies, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.1, .1)

        ## Image Handling ##
        self.image = Image()
        self.image.source = "Graphics/NPC/Alien1/Idle/Ship_01.png"
        self.image.allow_stretch = True
        self.add_widget(self.image)
        self.image.size_hint = (None, None)
        self.image.size = (dp(50), dp(50))
        
        ## Widget handling ##
        self.rotation = 0
        self.pos = pos
             
        ## Enemy class data ##
        anim_states = {'Dead': [], 'Move': [], 'Idle': []}
        self.animations = get_animations(anim_states, 'NPC', 'Alien1')
        self.enemies = enemies
        self.state = "Idle" 

        

    def init_pos(self, pos):
        ## Update position - Called from battle scene ##
        self.pos = pos

    def update(self, dt):
        pass