from game_settings import *
from ent_player import *
from ent_ai import *
from utilities import *
from proj_bullet import *

from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.image import Image

from os import walk

#######################
# Arena gameplay loop #
#######################

class Battle(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background = []
        self.world = []
        self.ships = []
        self.inactive_bullets = []
        self.bullet_group = []

        self.fps_count = 0
        self.total_fps = 0

        self.player = None
        self.half_width = self.width//2
        self.half_height = self.height//2

        Clock.schedule_interval(self.update, 1/FPS)

        self.draw_background()
        self.draw_player()
        self.draw_enemy()
        self.insantiate_bullets()

    def on_size(self, *args):
        pos = [self.width//2, self.height//2]
        self.player.init_pos(pos)

        for img in self.background:
            img.screen_size = [self.width, self.height]


#######################
# Background Handling #
#######################

    ## Init background images ##

    def draw_background(self):
        nebula = Image(source="Graphics/Backgrounds/Nebula/green.png")
        self.add_widget(nebula)
        print("Creating backgrounds")

        ## Images created in 2x2 Grid ##
        ## Grid coords for images: (0,0) (0,1) (1,0) (1,1)

        for i in range(2):
            for j in range(2):
                for _, _, images in walk('Graphics/Backgrounds/Stars/'):
                    for img in images:
                        stars = Stars(img, i, j)
                        self.add_widget(stars)
                        self.background.append(stars)


    def update_background(self, dt):

        ## Moves background images according to player velocity ##

        for sprite in self.background:
            offset_rate = .75

            ## Adjust offset rate for image type to create parallax effect ##
            if '02.png' in sprite.source:
                offset_rate = .25
            elif '03.png' in sprite.source:
                offset_rate = .05

            sprite.pos[0] += -self.player.velocity[0] * dt * offset_rate
            sprite.pos[1] += -self.player.velocity[1] * dt * offset_rate

            sprite.check_on_screen()
        
###################
# Player Handling #
###################
    def draw_player(self):

        ## Init player class ##

        self.player = Player(self.ships, self.inactive_bullets, self.bullet_group)
        self.add_widget(self.player)
        self.ships.append(self.player)
        print("Creating player")

    def update_player(self, dt):

        ## Calls player update function each frame ##

        self.player.update(dt)

##################
# Enemy handling #
##################
    def draw_enemy(self):

        ## Init test enemy ##

        pos = (50, 50)
        self.enemy = AI(pos, self.ships)
        self.add_widget(self.enemy)
        self.world.append(self.enemy)
        self.ships.append(self.enemy)
        print("Creating enemy")

    def update_enemy(self, dt):

        ## Move enemy ship position according to player velocity ##

        for enemy in self.world:
            pos = [enemy.pos[0], enemy.pos[1]]

            pos[0] += -self.player.velocity[0] * dt
            pos[1] += -self.player.velocity[1] * dt

            enemy.pos = pos

            enemy.update(dt)


#######################
# Projectile Handling #
#######################
    def insantiate_bullets(self):
        for bullet in range(50):
            bullet = Projectile("blue", None, 0, [5000, 5000])
            self.inactive_bullets.append(bullet)

    def update_projectiles(self, dt):
        ## Update bullets in active group ##

        ## Move bullet position according to player velocity ##
        for i, bullet in enumerate(self.bullet_group):
            pos = [bullet.pos[0], bullet.pos[1]]

            pos[0] += -self.player.velocity[0] * dt
            pos[1] += -self.player.velocity[1] * dt
            bullet.pos = pos

            ## Calls update function in bullet class ##

            bullet.update(dt)
            
            # Remove bullet if passed a certain distance / Outside of screen #
            if bullet.pos[0] < (self.width * -2):
                self.remove_active_bullet(bullet, i)

            elif bullet.pos[0] > (self.width * 2):
                self.remove_active_bullet(bullet, i)
            
            elif bullet.pos[1] < 0:
                self.remove_active_bullet(bullet, i)

            elif bullet.pos[1] > (self.height*2):
                self.remove_active_bullet(bullet, i)
                

    def remove_active_bullet(self, bullet, index):
    
        ## remove bullet from active bullets group - Add to inactive group - remove widget ##
        self.bullet_group.pop(index)
        self.inactive_bullets.append(bullet)
        self.remove_widget(bullet)

        



######################
# Main gameplay loop #
######################

    def update(self, dt):
        time_factor = dt * FPS

        self.update_background(time_factor)
        self.update_player(time_factor)
        self.update_enemy(time_factor)
        self.update_projectiles(time_factor)


        self.print_fps()


    def print_fps(self):
        ## Print FPS and Average FPS every frame ##
        fps = Clock.get_fps()
        self.fps_count += 1
        self.total_fps += fps
        average_fps = self.total_fps//self.fps_count
        print("FPS: ", fps, " / Average FPS: ", average_fps)


#########################################
# Class handles star paralax background #
#########################################

class Stars(Image):
    def __init__(self, img, x, y, **kwargs):
        super().__init__(**kwargs)
        
        self.screen_size = [0, 0]
        self.x = x
        self.y = y
        self.source = "Graphics/Backgrounds/Stars/" + img
        self.allow_stretch = True
        self.opacity = 1

    def on_size(self, *args):
        ## Updates BG image position after screen size is calculated ##
        x_pos = self.x * self.width
        y_pos = self.y * self.height

        self.pos = (x_pos, y_pos)

    def check_on_screen(self):

        ## Cycles background images to create repetitive effect ##
        if self.pos[0] > self.screen_size[0]:
            self.pos[0] = -self.width
        if (self.pos[0] + self.width) < 0:
            self.pos[0] = self.screen_size[0]
        
        if self.pos[1] > self.screen_size[1]:
            self.pos[1] = -self.height
        if (self.pos[1] + self.height) < 0:
            self.pos[1] = self.screen_size[1]
        

