"""As of 11/30, the charcter is capable of switching between the 'lanes' with
w/s, and able to move forwards or backwards in their lane with a/d. Pressing P
will cause one 'enemy' charcter to spawn in a random lane and move to the left.
They despawn if they leave the left side of the screen or the make contact with
the player avatar.There is no win or lose conditions yet as well. The images
used for the character and the enemies are just placeholder pictures I grabbed"""


import pygame, glob, random, time
from LabelClass import *
from pygame.locals import *

# CONSTANTS
WIDTH  = 1000  # Window width
HEIGHT = 600  # Window height
BLACK  = (0,0,0) # Colors
WHITE  = (255,255,255)
BACKGR = BLACK  # Background Color
FOREGR = WHITE  # Foreground Color
FPS    = 40 # Frames per second



class Player:

    def __init__(self, screen, centerx, 
      centery, speed,):
        self.surface = pygame.image.load('turtle.jpeg')
        self.rect = self.surface.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speed = speed
        self.screen = screen
        self.row = 1
        self.dir = ''
        

    def move(self):
        if self.dir != '':
            if self.dir == 'd' and self.row != 1:
                self.rect.top += 200
                self.row -= 1
                print self.rect.top
            if self.dir == 'u' and self.row != 3:
                self.rect.top -= 200
                self.row += 1
                print self.rect.top
            if self.dir == 'l' and self.rect.left > 0:
                self.rect.left -= self.speed
            if self.dir == 'r' and self.rect.right < WIDTH:
                self.rect.right += self.speed

    def draw(self):
        self.screen.blit(self.surface,self.rect)
        

class enemy:
    
    def __init__(self,screen,speed,top):
        self.surface = pygame.image.load('Ball.bmp')
        self.rect = self.surface.get_rect()
        self.rect.top = top
        self.rect.right = WIDTH
        self.speed = speed
        self.screen = screen
        # Basic enemy that will scroll to the left at a set speed

    def move(self):
        self.rect.left -= self.speed

    def draw(self):
        self.screen.blit(self.surface,self.rect)
        


class game:
    
    def __init__(self,screen):
        self.screen = screen
        self.Player = Player(self.screen,HEIGHT//2,WIDTH//2,10)
        pygame.display.update()
        self.won = False
        self.mainClock = pygame.time.Clock()
        self.enemies = []

    def update(self):
        self.screen.fill(BLACK)
        for e in self.enemies:
            if e.rect.right < 0:  
                self.enemies.remove(e)
            if self.Player.rect.colliderect(e.rect):
                self.enemies.remove(e)
        for e in self.enemies:
            e.move()
            e.draw()
        self.Player.move()
        self.Player.draw()
        pygame.display.update()
        
            
    def run(self):
        stop = False
        while not stop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    stop = True
                    return
                if event.type == KEYDOWN: # Keeps moving as long as key down
                    if event.key == ord('a'):
                        self.Player.dir = 'l'
                    if event.key == ord('d'):
                        self.Player.dir = 'r'
                    if event.key == ord('w'):
                        self.Player.dir = 'u'
                    if event.key == ord('s'):                     
                        self.Player.dir = 'd'
                if event.type == KEYUP:
                    if event.key == ord('q'):
                        stop = True
                    if event.key == K_ESCAPE:
                        stop = True
                    if event.key == ord('a'): # End repetition.
                        self.Player.dir = ''
                    if event.key == ord('d'):
                        self.Player.dir = ''
                    if event.key == ord('w'):
                        self.Player.dir = ''
                    if event.key == ord('s'):
                        self.Player.dir = ''
                    if event.key == ord('p'):
                        self.enemies.append(enemy(self.screen,8,(20+(random.randint(0,2)*200))))
            self.mainClock.tick(FPS)
            self.update()
            if self.Lost:
                stop = True


def intro(screen):
    screen.fill(BLACK)
    pygame.display.update()
    introtext = Label(screen,WIDTH//2,HEIGHT*7//8,26,
                      "This is the first version of our game. Hit any button to play",WHITE, BLACK)
    introtext.draw()
                        
gamescreen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Delivery game')

pygame.init()

stop = False

intro(gamescreen)

while not stop:
    for event in pygame.event.get():
        if event.type == QUIT:
            stop = True
        if event.type == KEYDOWN:
            game = game(gamescreen)
            game.run()
            intro(gamescreen)

pygame.quit()
