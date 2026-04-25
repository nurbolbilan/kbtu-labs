import pygame
import random

# --- Constants ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
INITIAL_SPEED = 5
FOOD_PER_LEVEL = 3  # Increase level after every 3 foods eaten


class Snake:
    def __init__(self):
        # Initial snake body: 3 blocks long
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"

    def move(self, grow=False):
        # Calculate new head position based on current direction
        head = list(self.body[0])
        if self.direction == "UP":
            head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head[1] += BLOCK_SIZE
        elif self.direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            head[0] += BLOCK_SIZE

        # Add new head to the body
        self.body.insert(0, head)

        # If snake didn't eat food, remove the last tail segment to simulate movement
        if not grow:
            self.body.pop()

    def draw(self, surface):
        # Draw each segment of the snake body
        for part in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (*part, BLOCK_SIZE, BLOCK_SIZE))


class Food:
    def __init__(self, snake_body):
        # Generate initial position avoiding the snake
        self.pos = self.generate_pos(snake_body)

    def generate_pos(self, snake_body):
        """Generates a random position that does not overlap with the snake body"""
        while True:
            # Align food position with the grid (multiples of BLOCK_SIZE)
            pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                   random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

            # Check if food is inside the snake
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        # Draw the food as a red square
        pygame.draw.rect(surface, (255, 0, 0), (*self.pos, BLOCK_SIZE, BLOCK_SIZE))


# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Levels & Speed")
font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

# Initialize game objects
snake = Snake()
food = Food(snake.body)

# Game state variables
score = 0
level = 1
speed = INITIAL_SPEED
running = True

# --- Main Game Loop ---
while running:
    # Fill background with black
    screen.fill((0, 0, 0))

    # 1. Event Handling (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Prevent snake from reversing directly (e.g., cannot go UP if currently going DOWN)
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"

    # 2. Food Collision Logic
    if snake.body[0] == food.pos:
        score += 1
        snake.move(grow=True)  # Move and add a segment (no pop())
        food = Food(snake.body)  # Generate new food at a valid location

        # 3. Level Up Logic
        if score % FOOD_PER_LEVEL == 0:
            level += 1
            speed += 2  # Increase game speed (frequency of updates)
    else:
        snake.move()  # Normal movement

    # 4. Wall and Self-Collision Check
    head = snake.body[0]
    # Check if head is out of screen borders
    out_of_bounds = (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT)
    # Check if head touched any part of its own body
    self_collision = head in snake.body[1:]

    if out_of_bounds or self_collision:
        running = False  # Game Over

    # 5. Rendering (Drawing)
    snake.draw(screen)
    food.draw(screen)

    # Render Score and Level text
    info_text = font.render(f"Score: {score}  Level: {level}  Speed: {speed}", True, (255, 255, 255))
    screen.blit(info_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Control game speed via clock tick
    clock.tick(speed)

pygame.quit()