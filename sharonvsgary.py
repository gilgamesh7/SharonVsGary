# https://realpython.com/pygame-a-primer/
# https://pygame.readthedocs.io/en/latest/index.html

import pygame
import random

import sys


# pygame locals for access to key coordinates
# https://pygame.readthedocs.io/en/latest/1_intro/intro.html
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Set up screen size constants
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

# Set up colours
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE_ABS_ZERO = (0,72,186)
AMARANTH = (229,43,80)

# Set up sounds
pygame.mixer.init()
# Background
pygame.mixer.music.load("keyboard.ogg")
pygame.mixer.music.play(loops=-1)

# Action specific
garySad = pygame.mixer.Sound("wilhelm.ogg")
garyHappy = pygame.mixer.Sound("burp.ogg")


# Player 1
class Gary(pygame.sprite.Sprite):
    def __init__(self):
        super(Gary,self).__init__()
        # self.surf = pygame.Surface((75,25))
        # self.surf.fill(BLUE_ABS_ZERO)
        self.avatar = pygame.image.load("Gary.PNG").convert()
        self.surf = pygame.transform.scale(self.avatar,(50,50))
        self.surf.set_colorkey(WHITE,RLEACCEL)
        self.rect=self.surf.get_rect()

    def updatePosition(self,pressed_keys) :
        # Check tuple for 1 in keypos
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
            garyHappy.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
            garyHappy.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
            garyHappy.play()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
            garyHappy.play()
        
        # Stop Gary from going off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



class Sharon(pygame.sprite.Sprite) :
    def __init__(self):
        super(Sharon,self).__init__()
        # self.surf = pygame.Surface((20,10))
        # self.surf.fill(AMARANTH)
        self.avatar = pygame.image.load("sharon.PNG").convert()
        self.surf = pygame.transform.scale(self.avatar,(75,50))
        self.surf.set_colorkey(WHITE,RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20,SCREEN_WIDTH+100),
                random.randint(0,SCREEN_HEIGHT)
            )
        ) 
        self.speed=random.randint(10,15)  

    def updatePosition(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

class ScrumBoard(pygame.sprite.Sprite):
    def __init__(self):
        super(ScrumBoard,self).__init__()
        self.avatar = pygame.image.load("scrumBoard.PNG").convert()
        self.surf = pygame.transform.scale(self.avatar,(150,100))
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def updatePosition(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < 0:
            self.kill

class GameCredits(pygame.sprite.Sprite):
    def __init__(self):
        super(GameCredits,self).__init__()
        self.surf = pygame.image.load("credits.PNG").convert()
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH)/2,
                (SCREEN_HEIGHT)/2
            )
        )

def main():
    try : 
        pygame.init()

        # draw game surface
        screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        pygame.display.set_caption('Sharon Stops Gary !') 

        # Create sprite groups
        allSpritesGroup = pygame.sprite.Group()
        sharonGroup = pygame.sprite.Group()
        scrumboardsGroup = pygame.sprite.Group()

        # Custom event for adding new Sharon
        ADDSHARON = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDSHARON, 1000)
        # Custom event for adding new Scrumboard
        ADDSCRUM = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDSCRUM, 2000)


        # Instatiate Sprites
        gary = Gary()
        allSpritesGroup.add(gary) # Add Gary to allSprites
        sharon = Sharon()
        scrumboard = ScrumBoard()

        # Initiate clock for frame rate
        clock = pygame.time.Clock()

        running=True
        while running:
            # Monitor events on surface
            for event in pygame.event.get():
                # if user has pressed key
                if event.type == KEYDOWN:
                     # if user hits escape, quit
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == ADDSHARON :
                    sharon = Sharon()
                    allSpritesGroup.add(sharon)
                    sharonGroup.add(sharon)
                elif event.type == ADDSCRUM :
                    scrumboard = ScrumBoard()
                    allSpritesGroup.add(scrumboard)
                    scrumboardsGroup.add(scrumboard)


            # get dictionary of pressed keys
            pressed_keys = pygame.key.get_pressed()
            # update sprite positions
            gary.updatePosition(pressed_keys)
            sharon.updatePosition()
            scrumboard.updatePosition()

            # Make screen white
            screen.fill(WHITE)

            # Draw Gary on screen
            # screen.blit(gary.surf,gary.rect)
            # Draw all sprites
            for gameSprite in allSpritesGroup:
                screen.blit(gameSprite.surf, gameSprite.rect)

            # stop game if Gary collides with Sharon
            if pygame.sprite.spritecollideany(gary,sharonGroup):
                gary.kill()
                garyHappy.stop()
                garySad.play()
                while pygame.mixer.get_busy():
                    pygame.time.delay(100)

                running = False

            # Refresh display
            pygame.display.flip()

            # Time feedback every cycle to clock
            clock.tick(100)

        # All done! Stop and quit the mixer.
        garySad.play()
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # show credits
        screen.fill(AMARANTH)
        credits=GameCredits()
        screen.blit(credits.surf,credits.rect)
        pygame.display.flip()

        pygame.time.delay(5000)
        pygame.quit()
    except:
        print(f"{sys.exc_info()}")

if __name__ == "__main__":
    main()