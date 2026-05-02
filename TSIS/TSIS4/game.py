import pygame
import random
from config import WIDTH, HEIGHT, BLOCK_SIZE


class Snake:
    """Represents the player-controlled snake."""

    def __init__(self, color):
        # Initial body: 3 segments placed horizontally
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.color = tuple(color)  # Ensure it's a tuple for pygame
        self.shield = False        # Shield power-up flag

    def move(self, grow=False):
        """Move the snake one step in the current direction.
        If grow=True, don't remove the tail (snake gets longer)."""
        head = list(self.body[0])
        if self.direction == "UP":    head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN":  head[1] += BLOCK_SIZE
        elif self.direction == "LEFT":  head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE
        self.body.insert(0, head)
        if not grow:
            self.body.pop()

    def draw(self, surface):
        """Draw each segment of the snake body.
        If the snake has a shield, draw a white border around each segment."""
        for i, part in enumerate(self.body):
            # Head is slightly brighter for visual distinction
            color = tuple(min(c + 40, 255) for c in self.color) if i == 0 else self.color
            pygame.draw.rect(surface, color, (*part, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, (0, 0, 0), (*part, BLOCK_SIZE, BLOCK_SIZE), 1)  # Grid border
            if self.shield:
                # White outline indicates active shield
                pygame.draw.rect(surface, (255, 255, 255), (*part, BLOCK_SIZE, BLOCK_SIZE), 2)


class GameObject:
    """Base class for all items that appear on the game field (food, poison, power-ups)."""

    def __init__(self, snake_body, obstacles, color):
        self.color = color
        self.pos = self.generate_pos(snake_body, obstacles)

    def generate_pos(self, snake_body, obstacles):
        """Randomly pick a grid position that doesn't overlap
        the snake body or any obstacle block."""
        while True:
            pos = [
                random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE,
            ]
            if pos not in snake_body and pos not in obstacles:
                return pos


class Food(GameObject):
    """Regular food item. Has a 20% chance to be 'special' (golden, worth 3 points).
    Special food disappears after 5 seconds."""

    def __init__(self, snake_body, obstacles):
        self.is_special = random.random() < 0.2
        self.weight = 3 if self.is_special else 1
        color = (255, 215, 0) if self.is_special else (255, 50, 50)
        super().__init__(snake_body, obstacles, color)
        # Special food has a timer; None means it never expires
        self.timer = pygame.time.get_ticks() + 5000 if self.is_special else None

    def is_expired(self):
        """Return True if this is special food that has timed out."""
        if self.timer is None:
            return False
        return pygame.time.get_ticks() > self.timer


class PoisonFood(GameObject):
    """Poison food item (dark red). Shortens the snake by 2 segments when eaten.
    If the snake length drops to 1 or below → game over."""

    def __init__(self, snake_body, obstacles):
        super().__init__(snake_body, obstacles, (180, 0, 0))
        # Poison disappears after 7 seconds if not eaten
        self.timer = pygame.time.get_ticks() + 7000

    def is_expired(self):
        """Return True if the poison has timed out and should be removed."""
        return pygame.time.get_ticks() > self.timer

    def draw(self, surface):
        """Draw poison with a skull-like 'X' marker."""
        x, y = self.pos
        pygame.draw.rect(surface, self.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        # Draw small X mark
        pygame.draw.line(surface, (255, 255, 255), (x + 3, y + 3), (x + BLOCK_SIZE - 3, y + BLOCK_SIZE - 3), 2)
        pygame.draw.line(surface, (255, 255, 255), (x + BLOCK_SIZE - 3, y + 3), (x + 3, y + BLOCK_SIZE - 3), 2)


class PowerUp(GameObject):
    """Temporary power-up item. Three types:
    - SPEED  (blue)  : increases snake speed for 5 seconds
    - SLOW   (cyan)  : decreases snake speed for 5 seconds
    - SHIELD (white) : blocks the next fatal collision once
    Disappears after 8 seconds if not collected."""

    TYPES = ['SPEED', 'SLOW', 'SHIELD']
    COLORS = {
        'SPEED':  (50,  50,  255),
        'SLOW':   (0,   220, 220),
        'SHIELD': (220, 220, 220),
    }
    LABELS = {'SPEED': 'S', 'SLOW': 'W', 'SHIELD': 'P'}

    def __init__(self, snake_body, obstacles):
        self.type = random.choice(self.TYPES)
        super().__init__(snake_body, obstacles, self.COLORS[self.type])
        # Power-up disappears from the field after 8 seconds
        self.field_timer = pygame.time.get_ticks() + 8000
        # Duration the effect lasts once collected (5 seconds)
        self.effect_duration = 5000

    def is_expired(self):
        """Return True if this power-up was never picked up and its field timer ran out."""
        return pygame.time.get_ticks() > self.field_timer

    def draw(self, surface, font):
        """Draw the power-up as a colored square with a letter label."""
        x, y = self.pos
        pygame.draw.rect(surface, self.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, (255, 255, 255), (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)
        label = font.render(self.LABELS[self.type], True, (0, 0, 0))
        surface.blit(label, (x + 4, y + 2))