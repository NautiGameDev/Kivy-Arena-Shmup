
from kivy.uix.scatter import Scatter
from kivy.metrics import dp

from utilities import *
from proj_bullet import *

##################################################################
## Ship handler                                                 ##
## Handles movement, animation, aiming, and firing of all ships ##
## Player and enemy ships all inherit this class                ##
##################################################################

class Ship(Scatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ## Turn off scatter widget adjusting ##
        self.do_scale = False
        self.do_translation = False
        self.do_rotation = False

        ## Movement handling ##
        self.dir = [0, 0]
        self.velocity = [0, 0]
        self.speed = 5
        self.acceleration_rate = .5

        ## Global position for the player
        ## Player ship is always center x/y of screen size.
        ## Uses global position instead for pseudo reference of player position
        self.global_position = [0, 0]

        ## Animation handling ##
        self.anim_index = 0
        self.anim_rate = 0.1

        ## Handles firerate through cool downs and booleans ##
        self.can_fire = True
        self.can_fire_cooldown = 100
        self.fire_clock = 0
        self.fire_tick_rate = 10


    def on_size(self, *args):
        pass

#######################
## Movement handling ##
#######################

    def move(self, dt):

        ## Gets x movement values from player input then calculates increasing velocity ##
        if self.dir[0] == -1 or self.dir[0] == 1:
            if abs(self.velocity[0]) < self.speed:
                self.velocity[0] += self.dir[0] * self.acceleration_rate

        ## If player not moving on X axis, gradually slows down velocity ##
        elif self.dir[0] == 0:
            if self.velocity[0] < 0:
                self.velocity[0] += 0.05
            elif self.velocity[0] > 0:
                self.velocity[0] -= 0.05

        if self.dir[1] == -1 or self.dir[1] == 1:
            if abs(self.velocity[1]) < self.speed:
                self.velocity[1] += self.dir[1] * self.acceleration_rate
        elif self.dir[1] == 0:
            if self.velocity[1] < 0:
                self.velocity[1] += 0.05
            elif self.velocity[1] > 0:
                self.velocity[1] -= 0.05
        

        ## Pseudo code for future coding - Not implemented ##
        #self.global_position[0] += self.velocity[0] * dt
        #self.global_position[1] += self.velocity[1] * dt

        #Add script to move enemies by velocity with actual position instead of global position
        # if self.type != "Player":
        #    set-up position variable
        #    self.pos = position

####################
## State Handling ##
####################

    def check_state(self):

        ## Checks for directional input on x/y axis and updates ship state if moving or idle ##

        dirs = [-1, 1]

        if self.dir[0] in dirs or self.dir[1] in dirs:
            self.state = "Move"
        else:
            self.state = "Idle"

########################
## Animation handling ##
########################

    def animate(self):
        
        ## Increase animation index by rate with limit of the length of animation list ##
        ## Upates source of image widget in player/enemy classes according to the anim index and state ##

        self.anim_index = (self.anim_index + self.anim_rate) % len(self.animations[self.state])
        self.image.source = self.animations[self.state][int(self.anim_index)]

############################
## Aim and Shoot handling ##
############################

    def aim(self, dt):
        ## Resets target ##
        self.target = None

        ## Finds the closest enemy within a set range - Sets target closest enemy ##
        for ship in self.enemies:
            if ship == self:
                pass
            else:
                prev_dist = 500
                distance = get_distance(self, ship)

                if distance < 500 and distance < prev_dist:
                    prev_dist = distance
                    self.target = ship

        ## Calculates angle between self and enemy ship - Updates ships rotation to look at enemy ##
        if self.target:
            angle, degrees = get_target_angle(self, self.target)
            self.rotation = degrees

        ## When out of range of targets, set ship rotation based on movement ##
        ## Will update to match joystick angles after implementation         ##
        elif not self.target:
            if self.dir[0] != 0 or self.dir[1] != 0:
                move_angle = [0,0]
                ship_center = get_center(self)
                move_angle[0] = ship_center[0] + (self.dir[0] * 25)
                move_angle[1] = ship_center[1] + (self.dir[1] * 25)
                

                angle, degrees = get_movement_angle(self, move_angle)
                self.rotation = degrees
    
    def fire(self):
        ## Auto fires when ship has target and fire not on cool down ##
        ## Retrieves first bullet obj from inactive bullet list and sets to active ##
        ## Adds widget to battle scene ##
        ## Updates bullet position, rotation, type, and team  ##
        ## Sets cool down timer ##
        if self.can_fire and self.target: 
            bullet = self.inactive_bullets[0]
            self.parent.add_widget(bullet)
            bullet.set_active("Blue", "Player", self.rotation, self.pos)
            self.inactive_bullets.pop(0)
            self.active_bullets.append(bullet)

            self.fire_clock = self.can_fire_cooldown
            self.can_fire = False

    def fire_cooldown(self, dt):
        ## Calculates and decreases fire cool down timer ##
        ## When timer is < 0, resets can_fire boolean
        if self.can_fire == False:
            if self.fire_clock > 0:
                self.fire_clock -= self.fire_tick_rate * dt

            if self.fire_clock <= 0:
                self.can_fire = True
                self.fire_clock = 0


            
