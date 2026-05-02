import pygame
from tools import (draw_menu, tool_rect, size_btn_rect,
                   flood_fill, save_canvas,
                   draw_shape_preview, commit_shape)

pygame.init()

FPS = 60
timer = pygame.time.Clock()

font_title = pygame.font.SysFont("Georgia", 25, bold=True)
font_tools = pygame.font.SysFont("Georgia", 19, bold=True)
font_text  = pygame.font.SysFont("Arial", 20)

TOOLS = ["Pencil", "Line", "Rect", "Circle", "Fill", "Text", "Eraser"]
PALETTE = [
    (0,0,0),    (255,255,255), (128,128,128), (255,0,0),
    (255,200,0),(0,200,0),     (0,128,0),     (0,200,200),
    (0,80,180), (100,0,200),   (200,0,150),   (139,69,19)
]
BRUSH_SIZES = [2, 5, 10]

# --- Active state ---
active_tool  = "Pencil"
active_color = (0, 0, 0)
active_size  = BRUSH_SIZES[0]

WIDTH, HEIGHT = 800, 600
MENU_W = 200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Separate drawing surface (menu is drawn on top of screen, not canvas)
canvas = pygame.Surface((WIDTH - MENU_W, HEIGHT))
canvas.fill((255, 255, 255))

# --- Drawing state ---
drawing     = False
last_pos    = None    # last point for pencil / eraser
shape_start = None    # anchor point for line / rect / circle

# --- Text tool state ---
text_pos   = None
text_input = ""

# ── Main loop ──────────────────────────────────────────────────────────────

run = True
while run:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (MENU_W, 0))   # paste canvas beside the menu

    mouse     = pygame.mouse.get_pos()
    on_canvas = mouse[0] > MENU_W
    c_mouse   = (mouse[0] - MENU_W, mouse[1])   # position relative to canvas

    # Cursor dot preview
    if on_canvas and active_tool not in ("Fill", "Text", "Eraser"):
        pygame.draw.circle(screen, active_color, mouse, max(active_size // 2, 2))

    # Live shape preview while dragging
    if drawing and shape_start:
        draw_shape_preview(screen, active_tool, shape_start, c_mouse, mouse,
                           active_color, active_size, MENU_W)

    # Text cursor preview
    if active_tool == "Text" and text_pos is not None:
        preview = font_text.render(text_input + "|", True, active_color)
        screen.blit(preview, (text_pos[0] + MENU_W, text_pos[1]))

    # Draw the menu and get clickable rects back
    color_rects, size_btns = draw_menu(
        screen, TOOLS, PALETTE, BRUSH_SIZES,
        active_tool, active_color, active_size,
        MENU_W, HEIGHT, font_title, font_tools
    )

    # ── Events ──────────────────────────────────────────────────────────────

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # ── Keyboard ────────────────────────────────────────────────────────
        if event.type == pygame.KEYDOWN:

            # Brush size shortcuts
            if event.key == pygame.K_1:   active_size = BRUSH_SIZES[0]
            elif event.key == pygame.K_2: active_size = BRUSH_SIZES[1]
            elif event.key == pygame.K_3: active_size = BRUSH_SIZES[2]

            # Ctrl+S → save
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas)

            # Text tool input
            if active_tool == "Text" and text_pos is not None:
                if event.key == pygame.K_RETURN:
                    rendered = font_text.render(text_input, True, active_color)
                    canvas.blit(rendered, text_pos)
                    text_pos   = None
                    text_input = ""
                elif event.key == pygame.K_ESCAPE:
                    text_pos   = None
                    text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        # ── Mouse button down ────────────────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Color palette
            for i, rect in enumerate(color_rects):
                if rect.collidepoint(event.pos):
                    active_color = PALETTE[i]

            # Tool buttons
            for i, name in enumerate(TOOLS):
                if tool_rect(i).collidepoint(event.pos):
                    active_tool = name

            # Brush size buttons
            for i, btn in enumerate(size_btns):
                if btn.collidepoint(event.pos):
                    active_size = BRUSH_SIZES[i]

            # Canvas actions
            if on_canvas:
                if active_tool in ("Pencil", "Eraser"):
                    drawing  = True
                    last_pos = c_mouse

                elif active_tool in ("Line", "Rect", "Circle"):
                    drawing     = True
                    shape_start = c_mouse

                elif active_tool == "Fill":
                    if 0 <= c_mouse[0] < canvas.get_width() and \
                       0 <= c_mouse[1] < canvas.get_height():
                        flood_fill(canvas, c_mouse[0], c_mouse[1], active_color)

                elif active_tool == "Text":
                    text_pos   = c_mouse
                    text_input = ""

        # ── Mouse button up ──────────────────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and on_canvas and shape_start:
                commit_shape(canvas, active_tool, shape_start,
                             c_mouse, active_color, active_size)
            drawing     = False
            last_pos    = None
            shape_start = None

        # ── Mouse motion ─────────────────────────────────────────────────────
        if event.type == pygame.MOUSEMOTION:
            if drawing and on_canvas:
                if active_tool == "Pencil" and last_pos:
                    pygame.draw.line(canvas, active_color,
                                     last_pos, c_mouse, active_size)
                    last_pos = c_mouse
                elif active_tool == "Eraser" and last_pos:
                    pygame.draw.line(canvas, (255, 255, 255),
                                     last_pos, c_mouse, active_size * 4)
                    last_pos = c_mouse

    pygame.display.update()
    timer.tick(FPS)

pygame.quit()