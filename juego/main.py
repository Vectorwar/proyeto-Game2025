"""This is a pilot test file for the juego package.
create by Jose juan Padilla"""
import pygame
import random 
pygame.init()
#Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space rain game")
#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
#player properties
player_width = 50
player_height = 60
player = pygame.Rect(width // 2 - player_width // 2,
                     height - player_height - 10,
                     player_width,
                     player_height)
#meteor properties
meteor_width = 30
meteor_height = 30
meteors = []
#Game clock for controlling frame rate
clock = pygame.time.Clock()
# main loop of the game
running = True # game is running
while running: # this is a loop that keeps the game running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < height:
        player.y += 5
    
    # meteor generation
    if len(meteors) < 7:
        meteor = pygame.Rect(random.randint(0, width - meteor_width),
                             0, meteor_width, meteor_height)
        meteors.append(meteor)
    
    # meteor movement
    for meteor in meteors[:]:  
        meteor.y += 5
        if meteor.top > height:
            meteors.remove(meteor)
            
    # collision detection
    for meteor in meteors:
        if player.colliderect(meteor):
            running = False  # End the game on collision
    
    
    screen.fill(white) #fill the screen with white color
    pygame.draw.rect(screen, red, player) #draw the player rectangle
    for meteor in meteors:
        pygame.draw.rect(screen, red, meteor) #draw the meteor rectangle
    pygame.display.flip() #update the display
    clock.tick(60)  # Limit to 60 frames per second
pygame.quit()