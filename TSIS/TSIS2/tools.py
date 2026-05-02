import pygame
import datetime


# ── Layout helpers ─────────────────────────────────────────────────────────

def palette_rect(index, num_tools):
    """Return the Rect for a color swatch in the palette grid."""
    col = index % 4
    row = index // 4
    start_y = 45 + num_tools * 42 + 18
    return pygame.Rect(10 + col * 47, start_y + row * 45, 38, 38)

def tool_rect(i):
    """Return the Rect for a tool button at position i."""
    return pygame.Rect(10, 56 + 42 * i, 180, 32)

def size_btn_rect(i):
    """Return the Rect for a brush-size button (S / M / L)."""
    return pygame.Rect(12 + i * 62, 552, 52, 22)


# ── Draw the left menu ─────────────────────────────────────────────────────

def draw_menu(screen, TOOLS, PALETTE, BRUSH_SIZES,
              active_tool, active_color, active_size,
              MENU_W, HEIGHT,
              font_title, font_tools):
    """Draw the full left-side toolbar and return clickable rects."""

    pygame.draw.rect(screen, (200, 200, 200), [0, 0, MENU_W, HEIGHT])
    pygame.draw.line(screen, 'black', (MENU_W, 0), (MENU_W, HEIGHT), 2)

    # Title
    title = font_title.render("Paint", True, (0, 0, 0))
    screen.blit(title, (65, 8))
    pygame.draw.line(screen, (0, 0, 0), (0, 46), (MENU_W, 46))

    # Tool buttons — highlighted in blue when active
    for i, name in enumerate(TOOLS):
        r = tool_rect(i)
        bg = (140, 185, 255) if name == active_tool else (230, 230, 230)
        pygame.draw.rect(screen, bg, r, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), r, 1, border_radius=5)
        text = font_tools.render(name, True, (0, 0, 0))
        screen.blit(text, (r.x + 55, r.y + 5))

    # Separator before palette
    pygame.draw.line(screen, (0, 0, 0), (0, 350), (MENU_W, 350))

    # Color palette grid
    color_rects = []
    for i, c in enumerate(PALETTE):
        r = palette_rect(i, len(TOOLS))
        p = pygame.draw.rect(screen, c, r, border_radius=3)
        pygame.draw.rect(screen, (80, 80, 80), r, 1, border_radius=3)
        color_rects.append(p)

    # Active color preview
    pygame.draw.line(screen, (0, 0, 0), (0, 492), (MENU_W, 492))
    cr = pygame.Rect(10, 502, 100, 28)
    pygame.draw.rect(screen, active_color, cr, border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), cr, 1, border_radius=5)
    label = font_tools.render("Color", True, (0, 0, 0))
    screen.blit(label, (118, 505))

    # Brush size buttons: S / M / L
    pygame.draw.line(screen, (0, 0, 0), (0, 540), (MENU_W, 540))
    size_btns = []
    for i, lbl in enumerate(["S", "M", "L"]):
        r = size_btn_rect(i)
        bg = (140, 185, 255) if BRUSH_SIZES[i] == active_size else (230, 230, 230)
        pygame.draw.rect(screen, bg, r, border_radius=4)
        pygame.draw.rect(screen, (0, 0, 0), r, 1, border_radius=4)
        t = font_tools.render(lbl, True, (0, 0, 0))
        screen.blit(t, (r.x + 18, r.y + 2))
        size_btns.append(r)

    return color_rects, size_btns


# ── Flood fill (BFS) ───────────────────────────────────────────────────────

def flood_fill(surface, x, y, new_color):
    """Fill a connected region of the same color starting at (x, y).

    Uses BFS with get_at / set_at; stops at pixels of a different color.
    """
    old_color = surface.get_at((x, y))[:3]
    new_color = tuple(new_color[:3])
    if old_color == new_color:
        return  # already this color — nothing to do

    w, h = surface.get_size()
    stack   = [(x, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        if cx < 0 or cx >= w or cy < 0 or cy >= h:
            continue
        if surface.get_at((cx, cy))[:3] != old_color:
            continue  # hit a boundary

        surface.set_at((cx, cy), new_color)
        visited.add((cx, cy))

        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))


# ── Save canvas ────────────────────────────────────────────────────────────

def save_canvas(canvas):
    """Save the canvas surface as a timestamped PNG file."""
    ts       = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{ts}.png"
    pygame.image.save(canvas, filename)
    print(f"Saved: {filename}")


# ── Shape preview (drawn on screen, not canvas) ────────────────────────────

def draw_shape_preview(screen, active_tool, shape_start, c_mouse, mouse,
                       active_color, active_size, MENU_W):
    """Draw a live ghost of the shape being dragged before mouse release."""

    if active_tool == "Line":
        start_s = (shape_start[0] + MENU_W, shape_start[1])
        pygame.draw.line(screen, active_color, start_s, mouse, active_size)

    elif active_tool == "Rect":
        x = min(shape_start[0], c_mouse[0]) + MENU_W
        y = min(shape_start[1], c_mouse[1])
        w = abs(c_mouse[0] - shape_start[0])
        h = abs(c_mouse[1] - shape_start[1])
        pygame.draw.rect(screen, active_color, (x, y, w, h), active_size)

    elif active_tool == "Circle":
        cx = (shape_start[0] + c_mouse[0]) // 2 + MENU_W
        cy = (shape_start[1] + c_mouse[1]) // 2
        rx = abs(c_mouse[0] - shape_start[0]) // 2
        ry = abs(c_mouse[1] - shape_start[1]) // 2
        if rx > 0 and ry > 0:
            pygame.draw.ellipse(screen, active_color,
                                (cx - rx, cy - ry, rx * 2, ry * 2), active_size)


# ── Commit shape to canvas on mouse release ────────────────────────────────

def commit_shape(canvas, active_tool, shape_start, c_mouse, active_color, active_size):
    """Draw the finished shape permanently onto the canvas surface."""

    if active_tool == "Line":
        pygame.draw.line(canvas, active_color, shape_start, c_mouse, active_size)

    elif active_tool == "Rect":
        x = min(shape_start[0], c_mouse[0])
        y = min(shape_start[1], c_mouse[1])
        w = abs(c_mouse[0] - shape_start[0])
        h = abs(c_mouse[1] - shape_start[1])
        pygame.draw.rect(canvas, active_color, (x, y, w, h), active_size)

    elif active_tool == "Circle":
        cx = (shape_start[0] + c_mouse[0]) // 2
        cy = (shape_start[1] + c_mouse[1]) // 2
        rx = abs(c_mouse[0] - shape_start[0]) // 2
        ry = abs(c_mouse[1] - shape_start[1]) // 2
        if rx > 0 and ry > 0:
            pygame.draw.ellipse(canvas, active_color,
                                (cx - rx, cy - ry, rx * 2, ry * 2), active_size)