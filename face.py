import pygame
import sys

FUSCHIA = (255,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

def main():
    try :
        # initialize games package
        pygame.init()

        # set up 800X600 window 
        gameDisplay = pygame.display.set_mode([800,600])

        # set up window title
        pygame.display.set_caption('In God We Trust!')


        # Flag to be set if user quits the window
        closed = False

        while not closed :
            # Get stream of events
            for event in pygame.event.get():
                # As long as the event is not quit, print the event in python log
                if event.type == pygame.QUIT:
                    closed = True
                print(f"{event}")


            # set icon
            icon = pygame.image.load("Cat.JPG")
            pygame.display.set_icon(icon)

            # Set background colour
            gameDisplay.fill(FUSCHIA)

            #Draw face (surface,colour,centre,radius,fill/nofill)
            pygame.draw.circle(gameDisplay,WHITE,[430,350],200,0)

            # Draw Eye 1 Ellipse (surface,colour,x,y,length,breadth,fill/nofill)
            pygame.draw.ellipse(gameDisplay,BLACK,[350,250,50,100],0)

            # Draw Eye 2 Ellipse (surface,colour,x,y,length,breadth,fill/nofill)
            pygame.draw.ellipse(gameDisplay,BLACK,[450,250,50,100],0)

            # Draw Mouth Ellipse (surface,colour,x,y,length,breadth,fill/nofill)
            pygame.draw.ellipse(gameDisplay,BLACK,[300,400,250,50],0)

            # Update screen
            pygame.display.flip()
    except:
        print(f"{sys.exc_info()}")

if __name__ == "__main__":
    main()