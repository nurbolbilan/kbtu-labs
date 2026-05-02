import pygame
import random
from pygame.locals import *

WIDTH, HEIGHT = 400, 600
ROAD_LEFT  = 30
ROAD_RIGHT = 370

CAR_TINTS = {
    "red":   (255,  80,  80),
    "blue":  ( 80,  80, 255),
    "green": ( 80, 200,  80),
}


# ─────────────────────────── PLAYER ──────────────────────────────

class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="default"):
        super().__init__()
        base = pygame.image.load("assets/Player.png")
        base = pygame.transform.scale(base, (50, 90))

        if car_color in CAR_TINTS:
            tinted = base.copy()
            overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
            r, g, b = CAR_TINTS[car_color]
            overlay.fill((r, g, b, 80))
            tinted.blit(overlay, (0, 0))
            self.image = tinted
        else:
            self.image = base

        self.rect = self.image.get_rect(center=(200, 500))

        # Power-up state
        self.shield       = False
        self.nitro_active = 0    # frames remaining
        self.inv_timer    = 0    # brief invincibility after impact (frames)

    # ── power-up activations ──────────────────────────────────────
    def activate_nitro(self, frames=180):
        self.nitro_active = frames

    def activate_shield(self):
        self.shield = True

    def repair(self):
        """Instant: grants brief invincibility frames (clears slow effects)."""
        self.inv_timer = 120

    def is_invincible(self):
        return self.shield or self.inv_timer > 0

    # ── per-frame update ──────────────────────────────────────────
    def move(self):
        keys = pygame.key.get_pressed()
        speed = 9 if self.nitro_active > 0 else 5
        if self.nitro_active > 0:
            self.nitro_active -= 1
        if self.inv_timer > 0:
            self.inv_timer -= 1

        if (keys[K_LEFT]  or keys[K_a]) and self.rect.left  > ROAD_LEFT:
            self.rect.move_ip(-speed, 0)
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip( speed, 0)
        if (keys[K_UP]    or keys[K_w]) and self.rect.top   > 0:
            self.rect.move_ip(0, -speed)
        if (keys[K_DOWN]  or keys[K_s]) and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0,  speed)

    def draw_effects(self, screen):
        """Draw shield ring and nitro flames around the player."""
        if self.shield:
            pygame.draw.circle(screen, (100, 200, 255), self.rect.center, 36, 3)
        if self.nitro_active > 0:
            for i in range(3):
                x = self.rect.centerx - 8 + i * 8
                y = self.rect.bottom + random.randint(4, 18)
                pygame.draw.ellipse(screen, (255, 80 + i * 40, 0), (x - 4, y - 4, 8, 14))


# ─────────────────────────── ENEMY ───────────────────────────────

class Enemy(pygame.sprite.Sprite):
    _FALLBACK_COLORS = [
        (200, 50, 50), (50, 50, 200), (200, 180, 40),
        (50, 180, 50), (160, 50, 200),
    ]

    def __init__(self, speed, player_rect=None):
        super().__init__()
        try:
            img = pygame.image.load("assets/Enemy.png")
            self.image = pygame.transform.scale(img, (50, 90))
        except Exception:
            self.image = pygame.Surface((50, 90))
            self.image.fill(random.choice(self._FALLBACK_COLORS))

        self.rect  = self.image.get_rect()
        self.speed = speed
        self._safe_spawn(player_rect)

    def _safe_spawn(self, player_rect):
        for _ in range(20):
            x = random.randint(ROAD_LEFT + 25, ROAD_RIGHT - 25)
            self.rect.center = (x, -120)
            if player_rect is None or not self.rect.inflate(30, 30).colliderect(player_rect):
                return

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────────── COIN ────────────────────────────────

class Coin(pygame.sprite.Sprite):
    def __init__(self, player_rect=None):
        super().__init__()
        try:
            img = pygame.image.load("assets/coin.png")
            self.image = pygame.transform.scale(img, (28, 28))
        except Exception:
            self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 215, 0), (14, 14), 14)
            pygame.draw.circle(self.image, (200, 160, 0), (14, 14), 14, 2)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 14, ROAD_RIGHT - 14), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────── OBSTACLES ───────────────────────────────

class OilSpill(pygame.sprite.Sprite):
    """Slows the player momentarily (non-lethal)."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((64, 32), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, ( 20,  20,  60, 210), (0,  0, 64, 32))
        pygame.draw.ellipse(self.image, ( 60,  60, 120, 140), (8,  6, 48, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 32, ROAD_RIGHT - 32), -60)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill()


class Pothole(pygame.sprite.Sprite):
    """Non-lethal hazard that slows the player."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((44, 28), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, ( 40,  30,  20, 220), (0,  0, 44, 28))
        pygame.draw.ellipse(self.image, ( 70,  55,  30, 140), (6,  5, 32, 18))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 22, ROAD_RIGHT - 22), -60)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    """Lethal moving barrier (destroys car unless shielded)."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 22))
        self.image.fill((255, 140,  0))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 80, 22), 2)
        for i in range(4):                          # warning stripes
            pygame.draw.rect(self.image, (0, 0, 0), (i * 20, 0, 10, 22))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 40, ROAD_RIGHT - 40), -60)
        self._dir = random.choice([-1, 1])
        self._t   = 0

    def move(self, speed):
        self.rect.move_ip(0, speed)
        self._t += 1
        if self._t % 2 == 0:                        # drift side-to-side
            self.rect.move_ip(self._dir * 2, 0)
            if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
                self._dir *= -1
        if self.rect.top > HEIGHT:
            self.kill()


class NitroStrip(pygame.sprite.Sprite):
    """Road strip that grants a free nitro boost on drive-over."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((52, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 210, 0, 210), (0, 0, 52, 20), border_radius=4)
        f = pygame.font.SysFont("Verdana", 10, bold=True)
        self.image.blit(f.render("NITRO", True, (200, 60, 0)), (6, 4))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 26, ROAD_RIGHT - 26), -60)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────── POWER-UPS ───────────────────────────────

class PowerUp(pygame.sprite.Sprite):
    TYPES  = ["nitro", "shield", "repair"]
    COLORS = {"nitro": (255, 160,  20),
              "shield": ( 80, 200, 255),
              "repair": ( 80, 230, 100)}
    ICONS  = {"nitro": "N", "shield": "S", "repair": "R"}

    LIFETIME = 300   # frames before auto-despawn (~5 s)

    def __init__(self, kind=None):
        super().__init__()
        self.type = kind or random.choice(self.TYPES)

        self.image = pygame.Surface((38, 38), pygame.SRCALPHA)
        col = self.COLORS[self.type]
        pygame.draw.circle(self.image, col,          (19, 19), 19)
        pygame.draw.circle(self.image, (255,255,255),(19, 19), 19, 2)
        f = pygame.font.SysFont("Verdana", 17, bold=True)
        lbl = f.render(self.ICONS[self.type], True, (0, 0, 0))
        self.image.blit(lbl, lbl.get_rect(center=(19, 19)))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ROAD_LEFT + 19, ROAD_RIGHT - 19), -70)
        self.lifetime = self.LIFETIME

    def move(self, speed):
        self.rect.move_ip(0, speed)
        self.lifetime -= 1
        if self.rect.top > HEIGHT or self.lifetime <= 0:
            self.kill()