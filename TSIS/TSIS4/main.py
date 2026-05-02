import pygame
import sys
import random
from config import WIDTH, HEIGHT, BLOCK_SIZE, load_settings, save_settings
from db import DBManager
from game import Snake, Food, PoisonFood, PowerUp


# ──────────────────────────────────────────────────────────────────────────────
# Color palette used throughout the UI
# ──────────────────────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
YELLOW  = (255, 215, 0)
GRAY    = (100, 100, 100)
DGRAY   = (30,  30,  30)
GREEN   = (0,   200, 0)
RED     = (200, 0,   0)
CYAN    = (0,   220, 220)


class GameApp:
    """Main application class. Manages all game states and screens."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock   = pygame.time.Clock()
        self.db      = DBManager()
        self.settings = load_settings()

        # Two font sizes used across all screens
        self.font_lg = pygame.font.SysFont("Consolas", 26, bold=True)
        self.font_sm = pygame.font.SysFont("Consolas", 16)
        self.font_pu = pygame.font.SysFont("Consolas", 12, bold=True)  # power-up label

        # Login / session state
        self.username = ""
        self.user_id  = None

        # Game state machine: LOGIN → MENU → GAME | LEADERBOARD | SETTINGS | GAMEOVER
        self.state = "LOGIN"

        # These are set in start_game()
        self.snake      = None
        self.food       = None
        self.poison     = None
        self.powerup    = None          # At most one power-up on the field
        self.obstacles  = []
        self.score      = 0
        self.level      = 1
        self.speed      = 5
        self.pb         = 0

        # Active effect tracking: (effect_type, end_time)
        self.active_effect = None

        # Timer for spawning new power-ups
        self.next_powerup_spawn = 0

    # ──────────────────────────────────────────────────────────────────────────
    # Utility helpers
    # ──────────────────────────────────────────────────────────────────────────

    def draw_text(self, text, x, y, color=WHITE, center=False, font=None):
        """Render a text string onto the screen.
        If center=True, (x, y) is treated as the centre of the text."""
        font = font or self.font_lg
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)

    def draw_button(self, text, rect, hover=False):
        """Draw a simple rectangular button.
        Returns the pygame.Rect so callers can check mouse collision."""
        color = YELLOW if hover else GRAY
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        pygame.draw.rect(self.screen, WHITE, rect, 1, border_radius=6)
        surf = self.font_lg.render(text, True, BLACK if hover else WHITE)
        self.screen.blit(surf, surf.get_rect(center=rect.center))
        return rect

    # ──────────────────────────────────────────────────────────────────────────
    # LOGIN screen
    # ──────────────────────────────────────────────────────────────────────────

    def login_screen(self):
        """Prompt the player to type a username and press Enter."""
        self.screen.fill(BLACK)
        self.draw_text("SNAKE GAME", WIDTH // 2, 80, YELLOW, center=True)
        self.draw_text("Enter your username:", WIDTH // 2, HEIGHT // 2 - 40, center=True, font=self.font_sm)
        # Blinking cursor effect using ticks
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        self.draw_text(self.username + cursor, WIDTH // 2, HEIGHT // 2, GREEN, center=True)
        self.draw_text("Press ENTER to continue", WIDTH // 2, HEIGHT - 40, GRAY, center=True, font=self.font_sm)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username.strip():
                    self.user_id = self.db.get_user_id(self.username.strip())
                    self.state = "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif len(self.username) < 20 and event.unicode.isprintable():
                    self.username += event.unicode

    # ──────────────────────────────────────────────────────────────────────────
    # MAIN MENU screen
    # ──────────────────────────────────────────────────────────────────────────

    def main_menu(self):
        """Display the main menu with Play, Leaderboard, Settings, and Quit options."""
        self.screen.fill(BLACK)
        self.draw_text("SNAKE", WIDTH // 2, 40, YELLOW, center=True)
        self.draw_text(f"Hello, {self.username}!", WIDTH // 2, 80, GREEN, center=True, font=self.font_sm)

        mx, my = pygame.mouse.get_pos()
        buttons = [
            ("Play",        pygame.Rect(WIDTH // 2 - 70, 120, 140, 40)),
            ("Leaderboard", pygame.Rect(WIDTH // 2 - 70, 175, 140, 40)),
            ("Settings",    pygame.Rect(WIDTH // 2 - 70, 230, 140, 40)),
            ("Quit",        pygame.Rect(WIDTH // 2 - 70, 285, 140, 40)),
        ]

        for label, rect in buttons:
            self.draw_button(label, rect, hover=rect.collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in buttons:
                    if rect.collidepoint(event.pos):
                        if label == "Play":          self.start_game()
                        elif label == "Leaderboard": self.state = "LEADERBOARD"
                        elif label == "Settings":    self.state = "SETTINGS"
                        elif label == "Quit":        pygame.quit(); sys.exit()

    # ──────────────────────────────────────────────────────────────────────────
    # GAME initialisation
    # ──────────────────────────────────────────────────────────────────────────

    def start_game(self):
        """Reset all game state and transition to the GAME screen."""
        self.snake      = Snake(self.settings["snake_color"])
        self.obstacles  = []
        self.food       = Food(self.snake.body, self.obstacles)
        self.poison     = PoisonFood(self.snake.body, self.obstacles)
        self.powerup    = None
        self.score      = 0
        self.level      = 1
        self.speed      = 5
        self.active_effect = None
        self.next_powerup_spawn = pygame.time.get_ticks() + 10000  # First power-up after 10 s
        self.pb         = self.db.get_pb(self.user_id)
        self.state      = "GAME"

    # ──────────────────────────────────────────────────────────────────────────
    # GAME OVER  — save result and show screen
    # ──────────────────────────────────────────────────────────────────────────

    def trigger_game_over(self):
        """Save the session and switch to the GAMEOVER screen."""
        self.db.save_game(self.user_id, self.score, self.level)
        if self.score > self.pb:
            self.pb = self.score  # Update local PB for display
        self.state = "GAMEOVER"

    def game_over_screen(self):
        """Display final score, level, personal best; offer Retry or Main Menu."""
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", WIDTH // 2, 60,  RED,   center=True)
        self.draw_text(f"Score : {self.score}",   WIDTH // 2, 120, WHITE, center=True, font=self.font_sm)
        self.draw_text(f"Level : {self.level}",   WIDTH // 2, 150, WHITE, center=True, font=self.font_sm)
        self.draw_text(f"Best  : {self.pb}",      WIDTH // 2, 180, YELLOW, center=True, font=self.font_sm)

        mx, my = pygame.mouse.get_pos()
        retry_rect = pygame.Rect(WIDTH // 2 - 70, 230, 140, 40)
        menu_rect  = pygame.Rect(WIDTH // 2 - 70, 285, 140, 40)
        self.draw_button("Retry",     retry_rect, hover=retry_rect.collidepoint(mx, my))
        self.draw_button("Main Menu", menu_rect,  hover=menu_rect.collidepoint(mx, my))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    self.start_game()
                elif menu_rect.collidepoint(event.pos):
                    self.state = "MENU"

    # ──────────────────────────────────────────────────────────────────────────
    # GAME loop — one frame
    # ──────────────────────────────────────────────────────────────────────────

    def run_game(self):
        """Execute one game frame: handle input, update state, draw everything."""
        now = pygame.time.get_ticks()

        # ── Background & grid ────────────────────────────────────────────────
        self.screen.fill(BLACK)
        if self.settings["grid_overlay"]:
            for x in range(0, WIDTH,  BLOCK_SIZE):
                pygame.draw.line(self.screen, DGRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(self.screen, DGRAY, (0, y), (WIDTH, y))

        # ── Input handling ───────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.trigger_game_over()
                return
            if event.type == pygame.KEYDOWN:
                d = self.snake.direction
                if event.key == pygame.K_UP    and d != "DOWN":  self.snake.direction = "UP"
                if event.key == pygame.K_DOWN  and d != "UP":    self.snake.direction = "DOWN"
                if event.key == pygame.K_LEFT  and d != "RIGHT": self.snake.direction = "LEFT"
                if event.key == pygame.K_RIGHT and d != "LEFT":  self.snake.direction = "RIGHT"
                if event.key == pygame.K_ESCAPE:
                    self.trigger_game_over()
                    return

        # ── Active power-up effect expiry ────────────────────────────────────
        if self.active_effect:
            effect_type, end_time = self.active_effect
            if now > end_time:
                # Revert whatever the effect changed
                if effect_type == "SPEED": self.speed = max(5, self.speed - 3)
                if effect_type == "SLOW":  self.speed = min(15, self.speed + 2)
                self.active_effect = None

        # ── Special food expiry ──────────────────────────────────────────────
        if self.food.is_expired():
            self.food = Food(self.snake.body, self.obstacles)

        # ── Poison expiry ────────────────────────────────────────────────────
        if self.poison and self.poison.is_expired():
            self.poison = PoisonFood(self.snake.body, self.obstacles)

        # ── Field power-up expiry or spawn ──────────────────────────────────
        if self.powerup and self.powerup.is_expired():
            self.powerup = None  # Remove uncollected power-up from the field
        if self.powerup is None and now >= self.next_powerup_spawn:
            self.powerup = PowerUp(self.snake.body, self.obstacles)
            # Schedule the next potential spawn 15–25 seconds later
            self.next_powerup_spawn = now + random.randint(15000, 25000)

        # ── Move snake ───────────────────────────────────────────────────────
        head = self.snake.body[0]
        grow = False

        # Check food collision before moving (head is the current front segment)
        if head == self.food.pos:
            self.score += self.food.weight
            grow = True
            self.food = Food(self.snake.body, self.obstacles)
            self._check_level_up()

        # Check poison collision
        if self.poison and head == self.poison.pos:
            # Shorten the snake by 2 segments
            self.snake.body = self.snake.body[:-2]
            if len(self.snake.body) <= 1:
                # Snake is too short — game over
                self.trigger_game_over()
                return
            self.poison = PoisonFood(self.snake.body, self.obstacles)

        # Check power-up collision
        if self.powerup and head == self.powerup.pos:
            self._apply_powerup(self.powerup, now)
            self.powerup = None

        self.snake.move(grow)

        # ── Collision detection (after move) ─────────────────────────────────
        head = self.snake.body[0]
        hit_wall = head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT
        hit_self = head in self.snake.body[1:]
        hit_obs  = head in self.obstacles

        if hit_wall or hit_self or hit_obs:
            if self.snake.shield:
                # Shield absorbs the first fatal collision and is consumed
                self.snake.shield = False
                # Push the head back one step so the snake doesn't sit on a wall
                self.snake.body.pop(0)
            else:
                self.trigger_game_over()
                return

        # ── Draw everything ──────────────────────────────────────────────────
        self.snake.draw(self.screen)

        # Food
        pygame.draw.rect(self.screen, self.food.color, (*self.food.pos, BLOCK_SIZE, BLOCK_SIZE))
        # Indicate remaining time on special food with a shrinking bar
        if self.food.timer:
            remaining = max(0, self.food.timer - now)
            bar_w = int(BLOCK_SIZE * remaining / 5000)
            pygame.draw.rect(self.screen, WHITE, (*self.food.pos, bar_w, 3))

        # Poison
        if self.poison:
            self.poison.draw(self.screen)

        # Power-up (if present)
        if self.powerup:
            self.powerup.draw(self.screen, self.font_pu)
            # Show time remaining on the field as a thin bar above it
            remaining = max(0, self.powerup.field_timer - now)
            bar_w = int(BLOCK_SIZE * remaining / 8000)
            pygame.draw.rect(self.screen, CYAN, (self.powerup.pos[0], self.powerup.pos[1] - 4, bar_w, 3))

        # Obstacles
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, (120, 120, 120), (*obs, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, (60, 60, 60), (*obs, BLOCK_SIZE, BLOCK_SIZE), 1)

        # ── HUD ──────────────────────────────────────────────────────────────
        self.draw_text(f"Score:{self.score}  Lvl:{self.level}  PB:{self.pb}", 6, 4, YELLOW, font=self.font_sm)
        if self.snake.shield:
            self.draw_text("SHIELD ACTIVE", WIDTH - 130, 4, WHITE, font=self.font_sm)
        if self.active_effect:
            eff, end = self.active_effect
            secs = max(0, (end - now) // 1000)
            self.draw_text(f"{eff}: {secs}s", WIDTH - 110, 20, CYAN, font=self.font_sm)

        pygame.display.flip()
        self.clock.tick(self.speed)

    def _check_level_up(self):
        """Increase the level and speed every 10 points.
        From level 3 onward, add a random obstacle block each level."""
        new_level = self.score // 10 + 1
        if new_level > self.level:
            self.level  = new_level
            self.speed  = min(20, self.speed + 1)  # Cap speed at 20 fps
            if self.level >= 3:
                # Place a new obstacle, ensuring it doesn't land on the snake or food
                forbidden = list(self.snake.body) + [self.food.pos]
                if self.poison: forbidden.append(self.poison.pos)
                while True:
                    obs = [
                        random.randrange(1, WIDTH  // BLOCK_SIZE - 1) * BLOCK_SIZE,
                        random.randrange(1, HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE,
                    ]
                    if obs not in forbidden and obs not in self.obstacles:
                        self.obstacles.append(obs)
                        break

    def _apply_powerup(self, pu, now):
        """Apply the collected power-up effect to the game state."""
        if pu.type == "SPEED":
            self.speed += 3
            self.active_effect = ("SPEED", now + pu.effect_duration)
        elif pu.type == "SLOW":
            self.speed = max(3, self.speed - 2)
            self.active_effect = ("SLOW", now + pu.effect_duration)
        elif pu.type == "SHIELD":
            self.snake.shield = True
            # Shield lasts until triggered, no timed effect needed

    # ──────────────────────────────────────────────────────────────────────────
    # LEADERBOARD screen
    # ──────────────────────────────────────────────────────────────────────────

    def show_leaderboard(self):
        """Fetch and display the top 10 all-time scores from the database."""
        self.screen.fill(BLACK)
        self.draw_text("TOP 10 LEADERBOARD", WIDTH // 2, 24, YELLOW, center=True, font=self.font_sm)

        # Column headers
        self.draw_text("#",    30,  55, GRAY, font=self.font_sm)
        self.draw_text("User", 60,  55, GRAY, font=self.font_sm)
        self.draw_text("Score",260, 55, GRAY, font=self.font_sm)
        self.draw_text("Lvl",  360, 55, GRAY, font=self.font_sm)
        self.draw_text("Date", 420, 55, GRAY, font=self.font_sm)
        pygame.draw.line(self.screen, GRAY, (20, 72), (WIDTH - 20, 72), 1)

        top_scores = self.db.get_top_10()
        for i, (user, score, level, date) in enumerate(top_scores):
            y   = 80 + i * 28
            col = YELLOW if i == 0 else WHITE
            date_str = date.strftime("%d.%m.%y") if date else "-"
            self.draw_text(str(i + 1),    30,  y, col, font=self.font_sm)
            self.draw_text(user[:12],      60,  y, col, font=self.font_sm)
            self.draw_text(str(score),    260,  y, col, font=self.font_sm)
            self.draw_text(str(level),    360,  y, col, font=self.font_sm)
            self.draw_text(date_str,      420,  y, col, font=self.font_sm)

        # Back button
        mx, my = pygame.mouse.get_pos()
        back_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 45, 100, 32)
        self.draw_button("Back", back_rect, hover=back_rect.collidepoint(mx, my))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_m, pygame.K_ESCAPE):
                self.state = "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    self.state = "MENU"

    # ──────────────────────────────────────────────────────────────────────────
    # SETTINGS screen
    # ──────────────────────────────────────────────────────────────────────────

    def show_settings(self):
        """Let the player toggle grid/sound and change snake color, then save."""
        self.screen.fill(BLACK)
        self.draw_text("SETTINGS", WIDTH // 2, 30, YELLOW, center=True)

        mx, my = pygame.mouse.get_pos()

        # Grid toggle
        grid_rect = pygame.Rect(WIDTH // 2 - 80, 90, 160, 36)
        grid_label = f"Grid: {'ON' if self.settings['grid_overlay'] else 'OFF'}"
        self.draw_button(grid_label, grid_rect, hover=grid_rect.collidepoint(mx, my))

        # Sound toggle
        snd_rect = pygame.Rect(WIDTH // 2 - 80, 140, 160, 36)
        snd_label = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"
        self.draw_button(snd_label, snd_rect, hover=snd_rect.collidepoint(mx, my))

        # Snake color presets
        self.draw_text("Snake Color:", WIDTH // 2, 200, center=True, font=self.font_sm)
        color_options = [
            ("Green",  [0,   200, 0]),
            ("Blue",   [0,   100, 255]),
            ("Purple", [180, 0,   255]),
            ("Orange", [255, 140, 0]),
        ]
        for j, (name, rgb) in enumerate(color_options):
            cx = 80 + j * 130
            cr = pygame.Rect(cx, 220, 110, 32)
            hover = cr.collidepoint(mx, my)
            pygame.draw.rect(self.screen, tuple(rgb), cr, border_radius=5)
            pygame.draw.rect(self.screen, WHITE, cr, 2 if hover else 1, border_radius=5)
            self.draw_text(name, cr.centerx, cr.centery, WHITE, center=True, font=self.font_sm)

        # Save & Back button
        save_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 55, 140, 36)
        self.draw_button("Save & Back", save_rect, hover=save_rect.collidepoint(mx, my))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_rect.collidepoint(event.pos):
                    self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                elif snd_rect.collidepoint(event.pos):
                    self.settings["sound"] = not self.settings["sound"]
                elif save_rect.collidepoint(event.pos):
                    save_settings(self.settings)
                    self.state = "MENU"
                else:
                    for _, rgb in color_options:
                        cx = 80 + color_options.index((_, rgb)) * 130
                        cr = pygame.Rect(cx, 220, 110, 32)
                        if cr.collidepoint(event.pos):
                            self.settings["snake_color"] = rgb

    # ──────────────────────────────────────────────────────────────────────────
    # Main loop
    # ──────────────────────────────────────────────────────────────────────────

    def run(self):
        """Application entry point — dispatch to the correct screen each frame."""
        while True:
            if   self.state == "LOGIN":       self.login_screen()
            elif self.state == "MENU":        self.main_menu()
            elif self.state == "GAME":        self.run_game()
            elif self.state == "GAMEOVER":    self.game_over_screen()
            elif self.state == "LEADERBOARD": self.show_leaderboard()
            elif self.state == "SETTINGS":    self.show_settings()


if __name__ == "__main__":
    app = GameApp()
    app.run()