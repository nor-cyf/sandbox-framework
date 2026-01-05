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
    "idle":[subsprite(pygame.image.load("_Idle.png").convert(), 120, 80), 0.15],
    "running":[subsprite(pygame.image.load("_Run.png").convert(), 120, 80), 0.09],
    "jumping" : [subsprite(pygame.image.load("_Jump.png").convert(), 120, 80), 0.03],
    "falling" : [subsprite(pygame.image.load("_Fall.png").convert(), 120, 80), 0.03],

}

#animator class used during player intantiation, made to be used with different animation objects

class Animator:
    def __init__(self, animations):
        self.animations = animations
        self.frame_index = 0
        self.timer = 0
        self.last_state = None

    def update(self, dt, player):
        state = player.state
        frames, frame_speed = self.animations[state]
        
        if state != self.last_state:
            self.frame_index = 0 
            self.timer = 0
            self.last_state = state
        self.timer += dt
        if self.timer >= frame_speed:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
#refer to how you stored your animations

    def get_frame(self, player):
        state = player.state
        frames = self.animations[state][0]
        return frames[self.frame_index]


#Movement component to be plugged into the player class to then influence on player velocity etc

class Movement:
    def __init__ (self, speed = 200, jump_force = -400, gravity = 1000):
        self.speed = speed
        self.jump_force = jump_force
        self.gravity = gravity

    def handle_input(self, player, events):#to set a direction
        keys = pygame.key.get_pressed()
        player.direction.x = 0 

        if keys[pygame.K_a]:
            player.direction.x -= 1
        if keys[pygame.K_d]:
            player.direction.x += 1

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.velocity.y = self.jump_force


    def apply_physics(self, dt, player):
        #apply physics and update pos
        player.velocity.x = player.direction.x * self.speed
        player.velocity.y += self.gravity * dt 

        #update position
        player.pos.x += player.velocity.x * dt
        player.pos.y += player.velocity.y * dt


#player class
#creates a player object at a given pos

class Player:
    def __init__(self, pos, animator, movement):
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.state = "idle"
       
        self.animator = animator
        self.movement = movement

    def update_state(self):
        if self.velocity == (0, 0):
            self.state = "idle"


        elif self.velocity.x != 0:
            self.state = "running"

        elif self.velocity.y > 0:
            self.state = "falling"
        
        elif self.velocity.y < 0:
            self.state = "jumping"
    
    def update(self, dt, events):
        self.movement.handle_input(self, events)
        self.movement.apply_physics(dt, self)
        self.update_state()
        self.animator.update(dt, self)

    def draw(self, screen):
        sprite = self.animator.get_frame(self)
        screen.blit(sprite, self.pos)

        

    

    
player = Player((50, 50), Animator(animations), Movement())


#components, to move to separate files once writtten

##intantiate an Input object with a normalised direction vector













while True:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)
    player.update(dt, events)
    player.draw(screen)

    #collision_check
    #collision_correction
    #collision_opposite_force


    pygame.display.update()

    print(player.state)



