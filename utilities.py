import math

from os import walk

#######################################################
## High-use calculations used throughout the project ##
#######################################################

def get_center(sprite):
    
    ## Calculate center x/y coordinates of sprites ##

    pos = sprite.pos
    half_width = sprite.width//2
    half_height = sprite.height//2

    center = [pos[0] + half_width, pos[1] + half_height]
    return center

def get_animations(dict, type, level):

    ## Retrieves paths to image files and organizes in dictionary for animation handling ##

    animations = dict

    path = 'Graphics/' + type + "/" + level + "/"

    for state in animations:
        
        for _, _, images in walk(path + state):
            for img in images:
                new_path = path + state + "/" + img
                animations[state].append(new_path)

    return animations
    
def get_distance(unit, target):

    ## Calculates the distance between two objects based on center x/y coordinates ##

    s1 = get_center(unit)
    s2 = get_center(target)

    distance = math.sqrt((s2[0] - s1[0])**2 + (s2[1] - s1[1])**2)

    return distance

def get_target_angle(unit, target):

    ## Calculates the angle between two objects based on center x/y coordinates ##

    unit_center = get_center(unit)
    target_center = get_center(target)

    dx = target_center[0] - unit_center[0]
    dy = target_center[1] - unit_center[1]

    angle = math.atan2(dy, dx)
    degrees = math.degrees(angle) - 90
    
    return angle, degrees

def get_movement_angle(unit, coords):

    ## Calculates angle between object and coordinates ##

    unit_center = get_center(unit)

    dx = coords[0] - unit_center[0]
    dy = coords[1] - unit_center[1]
    angle = math.atan2(dy, dx)
    degrees = math.degrees(angle) - 90

    return angle, degrees
