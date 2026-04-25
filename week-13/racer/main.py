# Imports
import pygame, sys
from pygame.locals import *
import time
from things import Enemy, Player, Coin


# Initializing Pygame
pygame.init()

# Setting up FPS (Frames Per Second)
FPS = 60
FramePerSec = pygame.time.Clock()

# Defining color constants (R, G, B)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game configuration variables
WIDTH = 400
HEIGHT = 600
SPEED = 5
SCORE = [0]
COINS_SCORE = 0

# Setting up Fonts for text rendering
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Loading Background Image
# Ensure the 'images' folder exists in the same directory as this script
background = pygame.image.load("images/AnimatedStreet.png")
background = pygame.transform.scale(background, (400, 600))

# Initialize the display screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Sprite Instance Setup
player = Player()
enemy = Enemy()
coin = Coin()

# Creating Sprite Groups for collision and batch updates
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

# Custom User Event to increase speed every 1000ms (1 second)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Main Game Loop
while True:

    # Event Handling Loop
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw the background first (bottom layer)
    screen.blit(background, (0, 0))

    # Render and display the scores
    scores = font_small.render(str(SCORE[0]), True, BLACK)
    screen.blit(scores, (10, 10))

    coins_scores = font_small.render(str(COINS_SCORE), True, BLACK)
    screen.blit(coins_scores, (WIDTH - 40, 10))

    # Update positions and draw all active sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

        if isinstance(entity, Enemy):
            entity.move(SPEED, SCORE)
        else:
            entity.move()

    # Draw the coin separately
    screen.blit(coin.image, coin.rect)

    # Collision Detection: Player vs Enemies
    if pygame.sprite.spritecollideany(player, enemies):
        time.sleep(0.5)

        screen.fill(RED)
        screen.blit(game_over, (30, 250))

        pygame.display.update()
        # Clean up sprites before quitting
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Collision Detection: Player vs Coins
    if pygame.sprite.spritecollideany(player, coins):
        COINS_SCORE += 1
        coin.spawn()

    # Refresh the display
    pygame.display.update()
    # Lock the framerate to 60 FPS
    FramePerSec.tick(FPS)