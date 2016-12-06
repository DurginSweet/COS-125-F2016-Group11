"""As of 11/30, the charcter is capable of switching between the 'lanes' with
w/s, and able to move forwards or backwards in their lane with a/d. Pressing P
will cause one 'enemy' charcter to spawn in a random lane and move to the left.
They despawn if they leave the left side of the screen or the make contact with
the player avatar.There is no win or lose conditions yet as well. The images
used for the character and the enemies are just placeholder pictures I grabbed

12/5: The avatar now will only move up or down if the button is released, so that
the player can more easily move to the middle lane. Enemys are now added periodically
into random lanes as well. The new variables distance in the game class and movspeed in 
the player class track the progress towards the level's comlettion, while the global variable
levelnum tracks the level itself."""


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
FPS    = 30 # Frames per second



class Player:

    def __init__(self, screen, centerx, 
      centery, speed):
        self.surface = pygame.image.load('turtle.jpeg')
        self.rect = self.surface.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speed = speed
        self.screen = screen
        self.row = 1
        self.dir = ''
        self.movspeed = 1
        #movspeed is how far you move towards the end every frame
        

    def move(self):
        if self.dir != '':
            if self.dir == 'd' and self.row != 1:
                self.rect.top += 200
                self.row -= 1
                self.dir = ''
            if self.dir == 'u' and self.row != 3:
                self.rect.top -= 200
                self.row += 1
                self.dir = ''
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
        


class Game:
    
    def __init__(self,screen,levelnum):
        self.screen = screen
        self.Player = Player(self.screen,HEIGHT//2,WIDTH//2,10)
        pygame.display.update()
        self.won = False
        self.lose = False
        self.mainClock = pygame.time.Clock()
        self.enemies = []
        self.levelnum = levelnum
        self.distance = 0

    def update(self):
        self.screen.fill(BLACK)
        if self.Player.movspeed < 5:
            self.Player.movspeed += 1 #steadily increases the players passivee speed towards the end if they avaoid obsticals
            #this may be altered later for game balance or something
        for e in self.enemies:
            if e.rect.right < 0:  
                self.enemies.remove(e)
            if self.Player.rect.colliderect(e.rect):
                self.enemies.remove(e)
                self.Player.movspeed = 1
                # Resets your movement speed back to one if you hit anything, to penalize the player
                print self.Player.movspeed
        for e in self.enemies:
            e.move()
            e.draw()
        self.Player.move()
        self.Player.draw()
        if self.Player.movspeed < 5:
            self.Player.movspeed += 1
        pygame.display.update()
        
        
            
    def run(self):
        stop = False
        pygame.time.set_timer(USEREVENT + 2, 1000)
        pygame.time.set_timer(USEREVENT + 1, 2000)
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
                        self.Player.dir = 'u'
                    if event.key == ord('s'):                     
                        self.Player.dir = 'd'
                if event.type == USEREVENT + 1:
                    for i in range((self.levelnum/10)+1):
                        if len(self.enemies) < 8:
                            self.enemies.append(enemy(self.screen,(random.randint(12,25)),(20+(random.randint(0,2)*200))))
                if event.type == USEREVENT + 2:
                    if len(self.enemies) < 6 + levelnum/10:
                        self.enemies.append(enemy(self.screen,(random.randint(6,12)),(20+(random.randint(0,2)*200))))
            self.distance += self.Player.movspeed 
            # distance increases with every frame meaning you 'move' forty times every second
            # right now it is set to take 10 seconds at the absolute slowest to completethe first level
            # And every level after that adds another 2 seconds, although it is likely to take much less time
            if self.distance > (80*(levelnum-1))+ 400:
                    self.won = True
                    stop = True
            self.mainClock.tick(FPS)
            self.update()
            
        if self.won == False:
            global levelnum
            self.enemies = []
            levelnum = 1
            self.screen.fill(BLACK)
            overtext = "Sorry, you lost."
            levelText = Label(self.screen,WIDTH//2,HEIGHT*7//8,26,overtext,WHITE, BLACK)
            levelText.draw()
            end = False
            while not end:
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == ord('p'):
                            end = True

            
            


def intro(screen):
    screen.fill(BLACK)
    pygame.display.update()
    introtext = Label(screen,WIDTH//2,HEIGHT*7//8,26,
                      "This is the first version of our game. Hit any button to play",WHITE, BLACK)
    introtext.draw()
                        
gamescreen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('RUN TIME')

pygame.init()

stop = False


intro(gamescreen)
levelnum = 1
while not stop:
    for event in pygame.event.get():
        if event.type == QUIT:
            stop = True
        if event.type == KEYUP:
            if event.key == ord('p'):
                game = Game(gamescreen,levelnum)
                game.run()
                if game.won == True:
                    game.enemies = []
                    levelnum += 1
                    game.screen.fill(BLACK)
                    text = "Congrats, press p to move on to level "+str(levelnum)+"!"
                    levelText = Label(game.screen,WIDTH//2,HEIGHT*7//8,26,text,WHITE, BLACK)
                    levelText.draw()
            if event.key == ord('q'):
                stop = True
pygame.quit()

