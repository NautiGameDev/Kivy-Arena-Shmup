import math
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.metrics import dp

from utilities import *

class Projectile(Scatter):
    def __init__(self, type, team, rotation, pos, **kwargs):
        super().__init__(**kwargs)
        
        ## Turn off scatter widget adjusting ##
        self.do_scale = False
        self.do_translation = False
        self.do_rotation = False

        ## Imports ##
        self.size_hint = (.01, .01)
        self.image_rotation = rotation
        self.travel_rotation = rotation + 90
        self.spawn_position = pos
        self.team = team

        ## Base Data ##
        self.state = "Base"
        self.speed = 15


        ## Animation handling (Currently not programmed) ##
        self.anim_states = {'Base': [], 'Hit': []}
        self.animations = get_animations(self.anim_states, 'Projectiles', type)
        self.anim_index = 0
        self.anim_rate = 0.1

        ## Sprite handling ##
        self.image = Image()
        self.image.source = self.animations[self.state][self.anim_index]
        self.image.allow_stretch = True
        self.add_widget(self.image)
        self.image.size_hint = (None, None)
        self.image.size = (dp(25), dp(25))

        ## Calculate basic x and y velocity based on object rotation ##
        self.x_velocity = math.cos(self.travel_rotation * (2*math.pi/360)) * self.speed
        self.y_velocity = math.sin(self.travel_rotation * (2*math.pi/360)) * self.speed

    def on_size(self, *args):
        ## Updates position when screen size is calculated ##
        self.spawn_position[0] = self.spawn_position[0] - self.image.width//2
        self.spawn_position[1] = self.spawn_position[1] - self.image.height//2
        self.pos = self.spawn_position
        self.rotation = self.image_rotation
    
    def set_active(self, type, team, rotation, pos):
        ## Updates the bullet data, position, and rotation when set to active ##
        self.state = "Base"
        self.team = team
        self.speed = 10

        ## Update position to attacking ship's position ##
        self.spawn_position[0] = pos[0] - self.image.width//2
        self.spawn_position[1] = pos[1] - self.image.height//2
        self.pos = self.spawn_position
        
        ## Image rotation, travel rotation, and x/y velocity calculations ##
        self.image_rotation = rotation
        self.rotation = self.image_rotation
        self.travel_rotation = rotation + 90
        self.x_velocity = math.cos(self.travel_rotation * (2*math.pi/360)) * self.speed
        self.y_velocity = math.sin(self.travel_rotation * (2*math.pi/360)) * self.speed

        ## Update animations dictionary based on projectile type ##
        self.animations = get_animations(self.anim_states, 'Projectiles', type)
        self.image.source = self.animations[self.state][self.anim_index]
        
#########################################
## Loop called every frame when active ##
#########################################

    def move(self, dt):
        ## Move bullet according to x/y velocity calculated from travel rotation ##
        dx = self.pos[0] + self.x_velocity * dt
        dy = self.pos[1] + self.y_velocity * dt

        direction = (dx, dy)
        self.pos = direction
        

    def update(self, dt):
        self.move(dt)


################################################################################
## Test projectile below - Testing performance of Image widget versus Scatter ##
################################################################################

class Projectile2(Image):
    def __init__(self, type, team, rotation, pos, **kwargs):
        super().__init__(**kwargs)

    
        self.travel_rotation = rotation + 90
        self.spawn_position = pos

        self.team = team
        self.state = "Base"
        self.speed = 10

        self.anim_states = {'Base': [], 'Hit': []}
        self.animations = get_animations(self.anim_states, 'Projectiles', type)
        self.anim_index = 0
        self.anim_rate = 0.1

        self.source = self.animations[self.state][self.anim_index]
        self.allow_stretch = True
        self.size_hint = (None, None)
        self.size = (dp(25), dp(25))

        self.x_velocity = math.cos(self.travel_rotation * (2*math.pi/360)) * self.speed
        self.y_velocity = math.sin(self.travel_rotation * (2*math.pi/360)) * self.speed

    def on_size(self, *args):
        self.spawn_position[0] = self.spawn_position[0] - self.width//2
        self.spawn_position[1] = self.spawn_position[1] - self.height//2
        self.pos = self.spawn_position
    
    def set_active(self, type, team, rotation, pos):
        self.state = "Base"
        self.team = team
        self.speed = 10

        self.spawn_position[0] = pos[0] - self.width//2
        self.spawn_position[1] = pos[1] - self.height//2
        self.pos = self.spawn_position
        
        self.travel_rotation = rotation + 90
        self.x_velocity = math.cos(self.travel_rotation * (2*math.pi/360)) * self.speed
        self.y_velocity = math.sin(self.travel_rotation * (2*math.pi/360)) * self.speed

        self.animations = get_animations(self.anim_states, 'Projectiles', type)
        self.source = self.animations[self.state][self.anim_index]
        

    def move(self, dt):
        dx = self.pos[0] + self.x_velocity * dt
        dy = self.pos[1] + self.y_velocity * dt

        direction = (dx, dy)
        self.pos = direction
        

    def update(self, dt):
        self.move(dt)