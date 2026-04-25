import pygame

# Constants for tools
TOOL_BRUSH = "brush"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint: 1-Brush, 2-Rect, 3-Circle, 4-Eraser | R,G,B,W-Colors")
    clock = pygame.time.Clock()

    # Editor state
    radius = 15
    current_color = (0, 0, 255)  # Default Blue
    current_tool = TOOL_BRUSH

    # List to store all drawn objects to keep them on screen
    # Structure: {'tool': str, 'color': tuple, 'points': list, 'radius': int}
    objects = []

    drawing = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # 1. Tool and Color Selection via Keyboard
            if event.type == pygame.KEYDOWN:
                # Color keys
                if event.key == pygame.K_r: current_color = (255, 0, 0)
                if event.key == pygame.K_g: current_color = (0, 255, 0)
                if event.key == pygame.K_b: current_color = (0, 0, 255)
                if event.key == pygame.K_w: current_color = (255, 255, 255)

                # Tool keys
                if event.key == pygame.K_1: current_tool = TOOL_BRUSH
                if event.key == pygame.K_2: current_tool = TOOL_RECT
                if event.key == pygame.K_3: current_tool = TOOL_CIRCLE
                if event.key == pygame.K_4: current_tool = TOOL_ERASER

            # 2. Mouse Interaction Logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to start drawing
                    drawing = True
                    start_pos = event.pos
                    # If eraser is selected, use background color (black)
                    color = (0, 0, 0) if current_tool == TOOL_ERASER else current_color

                    objects.append({
                        'tool': current_tool,
                        'color': color,
                        'points': [start_pos],
                        'radius': radius
                    })

                # 3. Brush Size Adjustment (Mouse Wheel)
                elif event.button == 4:  # Scroll Up
                    radius = min(100, radius + 1)
                elif event.button == 5:  # Scroll Down
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                curr_obj = objects[-1]
                if current_tool in [TOOL_BRUSH, TOOL_ERASER]:
                    # Continuous drawing for brush and eraser
                    curr_obj['points'].append(event.pos)
                else:
                    # For shapes, only store start and current (end) point
                    if len(curr_obj['points']) > 1:
                        curr_obj['points'][1] = event.pos
                    else:
                        curr_obj['points'].append(event.pos)

        # RENDERING
        screen.fill((0, 0, 0))  # Clear screen with black

        for obj in objects:
            pts = obj['points']
            if not pts: continue

            if obj['tool'] in [TOOL_BRUSH, TOOL_ERASER]:
                # Draw a smooth line by interpolating between points
                for i in range(len(pts) - 1):
                    drawLineBetween(screen, pts[i], pts[i + 1], obj['radius'], obj['color'])

            elif obj['tool'] == TOOL_RECT and len(pts) > 1:
                # Draw a rectangle outline
                rect_data = get_rect_tuple(pts[0], pts[1])
                pygame.draw.rect(screen, obj['color'], rect_data, min(obj['radius'], 5))

            elif obj['tool'] == TOOL_CIRCLE and len(pts) > 1:
                # Draw a circle (distance from start to end is radius)
                dx = pts[1][0] - pts[0][0]
                dy = pts[1][1] - pts[0][1]
                dist = int((dx ** 2 + dy ** 2) ** 0.5)
                pygame.draw.circle(screen, obj['color'], pts[0], dist, min(obj['radius'], 5))

        pygame.display.flip()
        clock.tick(120)


def get_rect_tuple(p1, p2):
    """Calculates top-left coordinates and dimensions for a rectangle."""
    x = min(p1[0], p2[0])
    y = min(p1[1], p2[1])
    w = abs(p1[0] - p2[0])
    h = abs(p1[1] - p2[1])
    return (x, y, w, h)


def drawLineBetween(screen, start, end, width, color):
    """Draws a solid line by filling gaps with small circles."""
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = i / iterations
        x = int((1 - progress) * start[0] + progress * end[0])
        y = int((1 - progress) * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


if __name__ == "__main__":
    main()