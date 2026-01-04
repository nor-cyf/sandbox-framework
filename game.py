#mid air control stops abruptly due to sudden velocity dropping to 0 (find a way to smooth it down)
#write proper code for collision to better it with time
#optimize
#learn to dockerise so it works on any laptop
#multiplayer so that two players can control and collide with latency management
import sys
import pygame
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Running') 
BG = (0, 0, 0)

#divides that sheet by the number of frames its got, returns a list of single sprites
def subsprite(sheet, frame_width, frame_height):
    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for i in range(sheet_width // frame_width):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = sheet.subsurface(rect).copy()
        frames.append(frame)
    return frames

#animations: as a dict of lists, the lists contain a list of frames and a frame duration
animations = {
    "idle":[subsprite(pygame.image.load("_Idle.png").convert(), 32, 32), 0.15],
    "running":[],
    "jumping" : [],
}


class Animator:
    def __init__(self, animations):
        self.animations = animations
        self.frame_index = 0
        self.timer = 0
        self.last_state = None

    def update(self, dt, player):
        state = player.state
        frames, frame_speed = self.animations[state]
        self.timer += dt
        
        if self.state != self.last_state:
            self.frame_index = 0 
            self.timer = 0
            self.last_state = self.state
        
        self.timer += dt
        if self.timer >= frame_speed:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
#refer to how you stored your animations

    def get_frame(self, player):
        state = player.state
        frames = self.animations[state][0]
        return frames[self.frame_index]
    
        

#player class
#creates a player object at a given pos

class Player:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.state = "idle"

    def update_state(self):
        if self.velocity == (0, 0):
            self.state = "idle"

        elif self.velocity.x > 0:
            self.state = "running"

        elif self.velocity.y > 0:
            self.state = "jumping"

    
player = Player((50, 50))


#components, to move to separate files once writtten

##intantiate an Input object with a normalised direction vector

class Input():
    def __init__(self):
        self.direction = pygame.math.Vector2()
    
    def update(self, keys):
        #resets the direction to check for new Input
        self.direction.xy = 0, 0


#sprite selection depending on the player state
#when idle, select animations.idle

class 












while True:
    dt = clock.tick(60) / 1000

    #key will be one if pressed and 0 if not
    keys = pygame.key.get_pressed():

    if keys[pygame.K_RIGHT]:
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)

    #collision_check
    #collision_correction
    #collision_opposite_force


    pygame.display.update()

