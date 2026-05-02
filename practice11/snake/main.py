import pygame, random

# Constants
W, H, BS = 600, 400, 20
SPEED, LIFETIME = 5, 5000
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)


class Snake:
    def __init__(self):
        self.body, self.dir = [[100, 100], [80, 100], [60, 100]], "RIGHT"

    def move(self, grow=False):
        h = list(self.body[0])
        if self.dir == "UP":
            h[1] -= BS
        elif self.dir == "DOWN":
            h[1] += BS
        elif self.dir == "LEFT":
            h[0] -= BS
        elif self.dir == "RIGHT":
            h[0] += BS
        self.body.insert(0, h)
        if not grow: self.body.pop()

    def draw(self, surf):
        for p in self.body: pygame.draw.rect(surf, GREEN, (*p, BS, BS))


class Food:
    def __init__(self, snake_body):
        self.pos = self.gen_pos(snake_body)
        self.weight = random.randint(1, 4)  # Random weight for size
        self.timer = pygame.time.get_ticks() + LIFETIME  # Always 5 seconds

    def gen_pos(self, snake_body):
        while True:
            p = [random.randrange(0, W // BS) * BS, random.randrange(0, H // BS) * BS]
            if p not in snake_body: return p

    def draw(self, surf):
        m = 10 - (self.weight * 2)  # Size based on weight
        pygame.draw.rect(surf, RED, (self.pos[0] + m, self.pos[1] + m, BS - m * 2, BS - m * 2))


# Setup
pygame.init()
scr = pygame.display.set_mode((W, H))
clock, font = pygame.time.Clock(), pygame.font.SysFont("Arial", 20)
snake, score, speed, run = Snake(), 0, SPEED, True
food = Food(snake.body)

while run:
    scr.fill(BLACK)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and snake.dir != "DOWN":
                snake.dir = "UP"
            elif e.key == pygame.K_DOWN and snake.dir != "UP":
                snake.dir = "DOWN"
            elif e.key == pygame.K_LEFT and snake.dir != "RIGHT":
                snake.dir = "LEFT"
            elif e.key == pygame.K_RIGHT and snake.dir != "LEFT":
                snake.dir = "RIGHT"

    # Timer and Eating logic
    if pygame.time.get_ticks() > food.timer: food = Food(snake.body)

    if snake.body[0] == food.pos:
        score += food.weight
        snake.move(grow=True)
        speed += 0.2
        food = Food(snake.body)
    else:
        snake.move()

    # Collisions
    h = snake.body[0]
    if h[0] < 0 or h[0] >= W or h[1] < 0 or h[1] >= H or h in snake.body[1:]: run = False

    # Render
    snake.draw(scr)
    food.draw(scr)
    t_left = max(0, (food.timer - pygame.time.get_ticks()) // 1000)
    txt = font.render(f"Score: {score} | Time: {t_left}s | Val: {food.weight}", True, WHITE)
    scr.blit(txt, (10, 10))
    pygame.display.flip()
    clock.tick(int(speed))

pygame.quit()