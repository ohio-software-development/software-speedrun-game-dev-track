# OUSDC Software Speedrun - Game Development Track
# code template adapted from www.pygame.org/docs/
import pygame

# pygame setup
pygame.init()
running = True
window = (1280, 720)
screen = pygame.display.set_mode(window)
clock = pygame.time.Clock()
dt = 0

# game loop
while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # your code here



    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # calculate delta time (dt) for framerate independent events (ie. physics)
    dt = clock.tick(60) / 1000 # cap at 60 fps

pygame.quit()
