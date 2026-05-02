import pygame, sys, time, random
from pygame.locals import *
from racer import *
from persistence import *
from ui import *

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Racer")
clock = pygame.time.Clock()

# ── fonts ──────────────────────────────────────────────────────────
F_SMALL  = pygame.font.SysFont("Verdana", 17)
F_MED    = pygame.font.SysFont("Verdana", 22, bold=True)
F_LARGE  = pygame.font.SysFont("Verdana", 32, bold=True)
F_TINY   = pygame.font.SysFont("Verdana", 14)

# ── assets ─────────────────────────────────────────────────────────
try:
    BG_IMG = pygame.image.load("assets/AnimatedStreet.png")
    BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))
except Exception:
    BG_IMG = pygame.Surface((WIDTH, HEIGHT))
    BG_IMG.fill((60, 60, 60))

# ── global state ───────────────────────────────────────────────────
STATE     = "MENU"
USER_NAME = "Player"
SETTINGS  = load_settings()

# ── difficulty presets ─────────────────────────────────────────────
DIFF = {
    "easy":   {"base_speed": 4, "enemy_max": 2, "obstacle_rate": 0.004},
    "normal": {"base_speed": 5, "enemy_max": 3, "obstacle_rate": 0.007},
    "hard":   {"base_speed": 7, "enemy_max": 5, "obstacle_rate": 0.013},
}

# ── colour helpers ─────────────────────────────────────────────────
COL_BG      = (25,  25,  40)
COL_PANEL   = (40,  40,  60, 200)
COL_GOLD    = (255, 215,  0)
COL_GREEN   = (60,  200,  80)
COL_RED     = (220,  60,  60)
COL_BLUE    = (70,  130, 200)
COL_GREY    = (130, 130, 150)


def draw_bg(bg_y):
    screen.blit(BG_IMG, (0, bg_y))
    screen.blit(BG_IMG, (0, bg_y - HEIGHT))


def draw_text(text, font, color, cx, cy):
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(cx, cy)))


def dark_overlay(alpha=160):
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, alpha))
    screen.blit(s, (0, 0))


def draw_panel(rect, color=(30, 30, 50, 210)):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill(color)
    screen.blit(s, rect.topleft)
    pygame.draw.rect(screen, (100, 100, 160), rect, 2, border_radius=10)


# ══════════════════════════════════════════════════════════════════
#  NAME ENTRY
# ══════════════════════════════════════════════════════════════════
def name_entry_screen():
    global USER_NAME, STATE
    inp = TextInput(100, 280, 200, 42, "Your name…")
    btn = Button(125, 360, 150, 44, "CONFIRM", COL_GREEN)

    bg_y = 0
    while True:
        bg_y = (bg_y + 2) % HEIGHT
        draw_bg(bg_y)
        dark_overlay(140)

        draw_text("ENTER YOUR NAME", F_LARGE, COL_GOLD, WIDTH // 2, 200)
        inp.draw(screen)
        btn.update(pygame.mouse.get_pos())
        btn.draw(screen)

        pygame.display.update()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()
            done = inp.handle_event(ev)
            if done or (ev.type == MOUSEBUTTONDOWN and btn.is_clicked(ev.pos)):
                USER_NAME = inp.get_text()
                STATE = "GAME"
                return


# ══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════
def main_menu():
    global STATE
    btns = [
        Button(100, 240, 200, 46, "PLAY",        COL_GREEN),
        Button(100, 300, 200, 46, "LEADERBOARD", COL_BLUE),
        Button(100, 360, 200, 46, "SETTINGS",    (120, 80, 180)),
        Button(100, 420, 200, 46, "QUIT",        COL_RED),
    ]
    bg_y = 0
    while STATE == "MENU":
        bg_y = (bg_y + 2) % HEIGHT
        draw_bg(bg_y)
        dark_overlay(130)

        draw_text("ROAD  RACER", F_LARGE, COL_GOLD, WIDTH // 2, 130)
        draw_text("Avoid traffic · Collect coins · Survive!", F_TINY, (180,180,220), WIDTH//2, 175)

        mx, my = pygame.mouse.get_pos()
        for b in btns:
            b.update((mx, my))
            b.draw(screen)

        pygame.display.update()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()
            if ev.type == MOUSEBUTTONDOWN:
                if btns[0].is_clicked(ev.pos):
                    STATE = "NAME"
                elif btns[1].is_clicked(ev.pos):
                    STATE = "LEADERBOARD"
                elif btns[2].is_clicked(ev.pos):
                    STATE = "SETTINGS"
                elif btns[3].is_clicked(ev.pos):
                    pygame.quit(); sys.exit()


# ══════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════
def settings_screen():
    global STATE, SETTINGS
    back = Button(125, 520, 150, 44, "BACK", COL_GREY)

    colors = ["default", "red", "blue", "green"]
    diffs  = ["easy", "normal", "hard"]
    bg_y   = 0

    while True:
        bg_y = (bg_y + 2) % HEIGHT
        draw_bg(bg_y)
        dark_overlay(150)

        draw_text("SETTINGS", F_LARGE, COL_GOLD, WIDTH // 2, 70)

        # ── Sound toggle ────────────────────────────────────────
        draw_text("Sound:", F_MED, (220, 220, 255), 80, 160)
        snd_lbl = "ON" if SETTINGS["sound"] else "OFF"
        snd_col = COL_GREEN if SETTINGS["sound"] else COL_RED
        snd_btn = Button(220, 144, 100, 36, snd_lbl, snd_col)
        snd_btn.update(pygame.mouse.get_pos())
        snd_btn.draw(screen)

        # ── Car colour ──────────────────────────────────────────
        draw_text("Car colour:", F_MED, (220, 220, 255), 80, 240)
        ci = colors.index(SETTINGS["car_color"])
        col_btn_l = Button(170, 224, 36, 36, "<", COL_BLUE)
        col_btn_r = Button(310, 224, 36, 36, ">", COL_BLUE)
        draw_text(SETTINGS["car_color"].capitalize(), F_MED, COL_GOLD, 255, 242)
        col_btn_l.update(pygame.mouse.get_pos())
        col_btn_r.update(pygame.mouse.get_pos())
        col_btn_l.draw(screen)
        col_btn_r.draw(screen)

        # ── Difficulty ──────────────────────────────────────────
        draw_text("Difficulty:", F_MED, (220, 220, 255), 80, 330)
        di = diffs.index(SETTINGS["difficulty"])
        dif_btn_l = Button(170, 314, 36, 36, "<", COL_BLUE)
        dif_btn_r = Button(310, 314, 36, 36, ">", COL_BLUE)
        draw_text(SETTINGS["difficulty"].capitalize(), F_MED, COL_GOLD, 255, 332)
        dif_btn_l.update(pygame.mouse.get_pos())
        dif_btn_r.update(pygame.mouse.get_pos())
        dif_btn_l.draw(screen)
        dif_btn_r.draw(screen)

        back.update(pygame.mouse.get_pos())
        back.draw(screen)
        pygame.display.update()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()
            if ev.type == MOUSEBUTTONDOWN:
                if snd_btn.is_clicked(ev.pos):
                    SETTINGS["sound"] = not SETTINGS["sound"]
                elif col_btn_l.is_clicked(ev.pos):
                    SETTINGS["car_color"] = colors[(ci - 1) % len(colors)]
                elif col_btn_r.is_clicked(ev.pos):
                    SETTINGS["car_color"] = colors[(ci + 1) % len(colors)]
                elif dif_btn_l.is_clicked(ev.pos):
                    SETTINGS["difficulty"] = diffs[(di - 1) % len(diffs)]
                elif dif_btn_r.is_clicked(ev.pos):
                    SETTINGS["difficulty"] = diffs[(di + 1) % len(diffs)]
                elif back.is_clicked(ev.pos):
                    save_settings(SETTINGS)
                    STATE = "MENU"
                    return


# ══════════════════════════════════════════════════════════════════
#  LEADERBOARD
# ══════════════════════════════════════════════════════════════════
def leaderboard_screen():
    global STATE
    back = Button(125, 540, 150, 44, "BACK", COL_GREY)
    board = load_data("leaderboard.json", [])
    bg_y  = 0

    while True:
        bg_y = (bg_y + 2) % HEIGHT
        draw_bg(bg_y)
        dark_overlay(160)

        draw_text("TOP  10", F_LARGE, COL_GOLD, WIDTH // 2, 55)

        hdrs = ["#", "Name", "Score", "Dist", "Coins"]
        xs   = [22, 60, 178, 255, 325]
        for xi, h in zip(xs, hdrs):
            draw_text(h, F_TINY, (180, 180, 220), xi, 95)

        pygame.draw.line(screen, (100, 100, 160), (15, 108), (385, 108), 1)

        for i, entry in enumerate(board[:10]):
            y   = 125 + i * 39
            row_col = COL_GOLD if i == 0 else (220, 220, 255)
            vals = [
                str(i + 1),
                entry.get("name",     "?")[:9],
                str(entry.get("score",    0)),
                str(entry.get("distance", 0)) + "m",
                str(entry.get("coins",    0)),
            ]
            for xi, v in zip(xs, vals):
                draw_text(v, F_TINY, row_col, xi, y)

        back.update(pygame.mouse.get_pos())
        back.draw(screen)
        pygame.display.update()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()
            if ev.type == MOUSEBUTTONDOWN and back.is_clicked(ev.pos):
                STATE = "MENU"
                return


# ══════════════════════════════════════════════════════════════════
#  GAME OVER
# ══════════════════════════════════════════════════════════════════
def game_over_screen(score, distance, coins):
    global STATE
    btn_retry = Button(60,  440, 130, 46, "RETRY",     COL_GREEN)
    btn_menu  = Button(210, 440, 130, 46, "MAIN MENU", COL_BLUE)
    bg_y = 0

    while True:
        bg_y = (bg_y + 2) % HEIGHT
        draw_bg(bg_y)
        dark_overlay(170)

        panel = pygame.Rect(50, 130, 300, 290)
        draw_panel(panel)

        draw_text("GAME  OVER", F_LARGE, COL_RED, WIDTH // 2, 165)
        draw_text(f"Score   : {score}",       F_MED, (220, 220, 255), WIDTH // 2, 230)
        draw_text(f"Distance: {int(distance)}m", F_MED, (220, 220, 255), WIDTH // 2, 268)
        draw_text(f"Coins   : {coins}",       F_MED, COL_GOLD,        WIDTH // 2, 306)
        draw_text(f"Player  : {USER_NAME}",   F_SMALL,(160, 160, 200), WIDTH // 2, 350)

        mx, my = pygame.mouse.get_pos()
        btn_retry.update((mx, my)); btn_retry.draw(screen)
        btn_menu.update((mx, my));  btn_menu.draw(screen)

        pygame.display.update()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()
            if ev.type == MOUSEBUTTONDOWN:
                if btn_retry.is_clicked(ev.pos):
                    STATE = "GAME"; return
                if btn_menu.is_clicked(ev.pos):
                    STATE = "MENU"; return


# ══════════════════════════════════════════════════════════════════
#  HUD helpers
# ══════════════════════════════════════════════════════════════════
PU_LABELS = {"nitro": "NITRO", "shield": "SHIELD", "repair": "REPAIR"}
PU_COLORS = {"nitro": (255,160,20), "shield": (80,200,255), "repair": (80,230,100)}

def draw_hud(score, distance, coins, active_pu, pu_timer, player):
    # top bar
    s = pygame.Surface((WIDTH, 38), pygame.SRCALPHA)
    s.fill((0, 0, 0, 140))
    screen.blit(s, (0, 0))

    screen.blit(F_SMALL.render(f"Score:{score}", True, (255,255,255)), (6, 10))
    screen.blit(F_SMALL.render(f"Dist:{int(distance)}m", True, (180,255,180)), (130, 10))

    # coin icon + count
    pygame.draw.circle(screen, COL_GOLD, (272, 18), 9)
    screen.blit(F_SMALL.render(str(coins), True, COL_GOLD), (286, 10))

    # active power-up
    if active_pu:
        lbl = PU_LABELS[active_pu]
        col = PU_COLORS[active_pu]
        secs = max(0, pu_timer // 60)
        txt = f"{lbl}  {secs}s" if active_pu != "shield" else lbl
        screen.blit(F_SMALL.render(txt, True, col), (310, 10))

    # nitro bar
    if player.nitro_active > 0:
        pct = player.nitro_active / 180
        bar_w = int(80 * pct)
        pygame.draw.rect(screen, (80, 80, 80), (10, HEIGHT - 14, 80, 8), border_radius=4)
        pygame.draw.rect(screen, (255, 160, 20), (10, HEIGHT - 14, bar_w, 8), border_radius=4)
        screen.blit(F_TINY.render("NITRO", True, (255,160,20)), (96, HEIGHT - 15))

    # shield indicator
    if player.shield:
        pygame.draw.circle(screen, (80, 200, 255), (20, HEIGHT - 34), 10, 3)


# ══════════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ══════════════════════════════════════════════════════════════════
def run_game():
    global STATE

    diff = DIFF.get(SETTINGS.get("difficulty", "normal"), DIFF["normal"])
    BASE_SPEED    = diff["base_speed"]
    ENEMY_MAX     = diff["enemy_max"]
    OBSTACLE_RATE = diff["obstacle_rate"]

    player = Player(SETTINGS.get("car_color", "default"))
    enemies   = pygame.sprite.Group()
    coins     = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()   # oil spills, potholes (non-lethal)
    hazards   = pygame.sprite.Group()   # barriers (lethal)
    nitro_strips = pygame.sprite.Group()
    powerups  = pygame.sprite.Group()

    all_visual = pygame.sprite.Group(player)

    score    = 0
    distance = 0.0
    coin_count = 0
    speed    = BASE_SPEED
    bg_y     = 0

    slow_timer   = 0     # frames player is slowed by oil/pothole
    active_pu    = None  # "nitro" | "shield" | "repair" | None
    pu_timer     = 0     # frames remaining for active power-up

    PU_DURATION  = {"nitro": 180, "shield": 9999, "repair": 1}

    spawn_timers = {"obstacle": 0, "hazard": 0, "nitro_strip": 0, "powerup": 0, "enemy": 0}
    # Minimum frames between enemy spawns (≈1.5 s at 60 fps)
    ENEMY_COOLDOWN = 90

    while True:
        # ── background scroll ──────────────────────────────────
        eff_speed = max(2, speed // 2) if slow_timer > 0 else speed // 2
        bg_y = (bg_y + eff_speed) % HEIGHT
        draw_bg(bg_y)

        # ── events ────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()

        # ── spawn enemies (one at a time, with cooldown) ───────
        spawn_timers["enemy"] += 1
        if len(enemies) < ENEMY_MAX and spawn_timers["enemy"] >= ENEMY_COOLDOWN:
            e = Enemy(speed, player.rect)
            enemies.add(e)
            all_visual.add(e)
            spawn_timers["enemy"] = 0

        # ── spawn coins ────────────────────────────────────────
        if len(coins) < 4 and random.random() < 0.025:
            c = Coin(player.rect)
            coins.add(c)
            all_visual.add(c)

        # ── spawn non-lethal obstacles ─────────────────────────
        spawn_timers["obstacle"] += 1
        if spawn_timers["obstacle"] > 90 and random.random() < OBSTACLE_RATE * 8:
            cls = random.choice([OilSpill, Pothole])
            obj = cls()
            obstacles.add(obj)
            all_visual.add(obj)
            spawn_timers["obstacle"] = 0

        # ── spawn barriers ────────────────────────────────────
        spawn_timers["hazard"] += 1
        if spawn_timers["hazard"] > 150 and random.random() < OBSTACLE_RATE * 5:
            b = Barrier()
            hazards.add(b)
            all_visual.add(b)
            spawn_timers["hazard"] = 0

        # ── spawn nitro strips ────────────────────────────────
        spawn_timers["nitro_strip"] += 1
        if spawn_timers["nitro_strip"] > 300 and random.random() < 0.008:
            ns = NitroStrip()
            nitro_strips.add(ns)
            all_visual.add(ns)
            spawn_timers["nitro_strip"] = 0

        # ── spawn power-ups ───────────────────────────────────
        spawn_timers["powerup"] += 1
        if spawn_timers["powerup"] > 360 and random.random() < 0.012 and active_pu is None:
            pu = PowerUp()
            powerups.add(pu)
            all_visual.add(pu)
            spawn_timers["powerup"] = 0

        # ── movement ──────────────────────────────────────────
        cur_speed = max(2, speed - 3) if slow_timer > 0 else speed
        if slow_timer > 0:
            slow_timer -= 1

        player.move()
        for e in enemies:      e.move(cur_speed)
        for c in coins:        c.move(cur_speed)
        for o in obstacles:    o.move(cur_speed)
        for h in hazards:      h.move(cur_speed)
        for ns in nitro_strips: ns.move(cur_speed)
        for pu in powerups:    pu.move(cur_speed)

        # ── distance & speed scaling ──────────────────────────
        distance += speed / 60.0
        speed = BASE_SPEED + int(distance) // 200

        # ── power-up timer ────────────────────────────────────
        if active_pu and active_pu != "shield":
            pu_timer -= 1
            if pu_timer <= 0:
                active_pu = None
                pu_timer  = 0

        # ── collision: enemies ────────────────────────────────
        if pygame.sprite.spritecollideany(player, enemies):
            if player.shield:
                player.shield = False
                active_pu = None
                player.inv_timer = 90
                # destroy the enemy we hit
                for e in pygame.sprite.spritecollide(player, enemies, True):
                    score += 5
            elif not player.is_invincible():
                update_leaderboard(USER_NAME, score, distance, coin_count)
                STATE = "GAMEOVER"
                return score, distance, coin_count

        # ── collision: barriers (lethal) ──────────────────────
        if pygame.sprite.spritecollideany(player, hazards):
            if player.shield:
                player.shield = False
                active_pu = None
                player.inv_timer = 90
                for h in pygame.sprite.spritecollide(player, hazards, True):
                    pass
            elif not player.is_invincible():
                update_leaderboard(USER_NAME, score, distance, coin_count)
                STATE = "GAMEOVER"
                return score, distance, coin_count

        # ── collision: non-lethal obstacles ───────────────────
        if pygame.sprite.spritecollideany(player, obstacles) and slow_timer == 0:
            slow_timer = 90
            for o in pygame.sprite.spritecollide(player, obstacles, True):
                pass

        # ── collision: nitro strips ───────────────────────────
        if pygame.sprite.spritecollideany(player, nitro_strips):
            for ns in pygame.sprite.spritecollide(player, nitro_strips, True):
                player.activate_nitro(180)

        # ── collision: coins ──────────────────────────────────
        for _ in pygame.sprite.spritecollide(player, coins, True):
            coin_count += 1
            score      += 2

        # ── collision: power-ups ──────────────────────────────
        for pu in pygame.sprite.spritecollide(player, powerups, True):
            if active_pu is None or pu.type != active_pu:
                active_pu = pu.type
                pu_timer  = PU_DURATION[pu.type]
                if pu.type == "nitro":
                    player.activate_nitro(180)
                elif pu.type == "shield":
                    player.activate_shield()
                elif pu.type == "repair":
                    player.repair()
                    slow_timer = 0
                    active_pu  = None

        # score ticks up with distance
        score = coin_count * 2 + int(distance) // 10

        # ── draw ──────────────────────────────────────────────
        # draw non-player sprites manually so we can add player effects on top
        for spr in all_visual:
            if spr is not player:
                screen.blit(spr.image, spr.rect)

        player.draw_effects(screen)
        screen.blit(player.image, player.rect)

        draw_hud(score, distance, coin_count, active_pu, pu_timer, player)

        # slow-down flash
        if slow_timer > 0 and slow_timer % 20 < 10:
            s2 = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s2.fill((0, 0, 150, 40))
            screen.blit(s2, (0, 0))

        pygame.display.update()
        clock.tick(60)


# ══════════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════════
while True:
    if STATE == "MENU":
        main_menu()
    elif STATE == "NAME":
        name_entry_screen()
    elif STATE == "GAME":
        result = run_game()
        if result:
            score, distance, coins = result
    elif STATE == "GAMEOVER":
        game_over_screen(score, distance, coins)
    elif STATE == "LEADERBOARD":
        leaderboard_screen()
    elif STATE == "SETTINGS":
        settings_screen()