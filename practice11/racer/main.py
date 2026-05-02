# Imports
from pygame import *
import pygame
import sys, time, random

# Initialize all imported pygame modules
pygame.init()

# Setting up FPS (Frames Per Second) controller
FPS = 60
FramePerSec = pygame.time.Clock()

# Game configuration and global variables
WIDTH = 400
HEIGHT = 600
bg_y = 0

SPEED = 5
SCORE = [0] # Using a list to pass the score by reference
COINS_SCORE = 0

# Setting up Fonts for text rendering
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, (0, 0, 0))

# Loading and scaling the Background Image
background = pygame.image.load("images/AnimatedStreet.png")
background = pygame.transform.scale(background, (400, 600))

# Initialize the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# Enemy class definition
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (75, 150))
        self.rect = self.image.get_rect()
        # Randomize starting position at the top
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self, current_speed, score_ref):
        # Move enemy down based on speed
        self.rect.move_ip(0, current_speed)
        # Reset position if it leaves the screen and increment score
        if (self.rect.top > 600):
            score_ref[0] += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

# Player class definition
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png")
        self.image = pygame.transform.scale(self.image, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        # Handle player movement with boundary checks
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin class definition
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("images/coin.png")
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.spawn()

    def move(self, current_speed, n):
        # Move coin down
        self.rect.move_ip(0, current_speed)
        # Respawn at the top if it passes the bottom boundary
        if (self.rect.top > 600):
            self.spawn()

    def spawn(self):
        # Randomize coin size and position
        size = random.randint(20, 70)
        # Scale from original_image to maintain quality
        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

# Create object instances
player = Player()
enemy = Enemy()
coin = Coin()

# Organize objects into Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

# Main Game Loop
while True:

    # Check for quit event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Create scrolling background effect
    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - 600))
    bg_y += 2
    if bg_y >= 600:
        bg_y = 0

    # Draw scores on screen
    scores_text = font_small.render(str(SCORE[0]), True, (0, 0, 0))
    screen.blit(scores_text, (10, 10))

    coins_text = font_small.render(str(COINS_SCORE), True, (0, 0, 0))
    screen.blit(coins_text, (WIDTH - 40, 10))

    # Iterate through all sprites to update movement and draw them
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        if isinstance(entity, (Enemy, Coin)):
            entity.move(SPEED, SCORE)
        else:
            entity.move()

    # Check for collision between Player and Enemies
    if pygame.sprite.spritecollideany(player, enemies):
        time.sleep(0.5)
        # Fill screen with red and show Game Over
        screen.fill((255, 0, 0))
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        # Clean up and exit
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check for collision between Player and Coins
    hits = pygame.sprite.spritecollide(player, coins, True)

    for hit in hits:
        COINS_SCORE += 1
        # Increase game difficulty speed when a coin is collected
        SPEED += 0.5
        # Spawn a new coin to replace the collected one
        new_coin = Coin()
        new_coin.spawn()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Update the full display surface to the screen
    pygame.display.update()
    # Limit the loop to run at 60 frames per second
    FramePerSec.tick(FPS)