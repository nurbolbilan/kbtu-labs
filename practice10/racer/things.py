import pygame
import random
from pygame.locals import *

WIDTH = 400
HEIGHT = 600
SPEED = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self, current_speed, score_ref):
        self.rect.move_ip(0, current_speed)
        if (self.rect.top > 600):
            score_ref[0] += 1  # Используем список для передачи по ссылке
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png")
        self.image = pygame.transform.scale(self.image, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, 5)
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/coin.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), random.randint(50, HEIGHT - 50))