import pygame
import math

# --- Constants for tools ---
TOOL_BRUSH = "brush"
TOOL_RECT = "rect"
TOOL_SQUARE = "square"
TOOL_CIRCLE = "circle"
TOOL_RTRIANGLE = "rtriangle"  # Right Triangle
TOOL_ETRIANGLE = "etriangle"  # Equilateral Triangle
TOOL_RHOMBUS = "rhombus"
TOOL_ERASER = "eraser"


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Paint | 1-4: Basic Tools | 5-8: Shapes | R,G,B,W: Colors")
    clock = pygame.time.Clock()

    # Editor state
    radius = 15
    current_color = (0, 0, 255)  # Default Blue
    current_tool = TOOL_BRUSH
    objects = []  # List to store all drawn objects
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
                if event.key == pygame.K_5: current_tool = TOOL_SQUARE
                if event.key == pygame.K_6: current_tool = TOOL_RTRIANGLE
                if event.key == pygame.K_7: current_tool = TOOL_ETRIANGLE
                if event.key == pygame.K_8: current_tool = TOOL_RHOMBUS

            # 2. Mouse Interaction Logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click start
                    drawing = True
                    start_pos = event.pos
                    color = (0, 0, 0) if current_tool == TOOL_ERASER else current_color

                    objects.append({
                        'tool': current_tool,
                        'color': color,
                        'points': [start_pos],
                        'radius': radius
                    })

                elif event.button == 4:  # Scroll Up (Increase size)
                    radius = min(100, radius + 1)
                elif event.button == 5:  # Scroll Down (Decrease size)
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                curr_obj = objects[-1]
                if current_tool in [TOOL_BRUSH, TOOL_ERASER]:
                    curr_obj['points'].append(event.pos)
                else:
                    # Update the second point (the end point) for shape preview
                    if len(curr_obj['points']) > 1:
                        curr_obj['points'][1] = event.pos
                    else:
                        curr_obj['points'].append(event.pos)

        # RENDERING
        screen.fill((0, 0, 0))

        for obj in objects:
            pts = obj['points']
            if not pts: continue

            tool = obj['tool']
            color = obj['color']
            thickness = max(1, min(obj['radius'] // 3, 10))  # Scale thickness for shapes

            if tool in [TOOL_BRUSH, TOOL_ERASER]:
                for i in range(len(pts) - 1):
                    drawLineBetween(screen, pts[i], pts[i + 1], obj['radius'], color)

            elif tool == TOOL_RECT and len(pts) > 1:
                pygame.draw.rect(screen, color, get_rect_tuple(pts[0], pts[1]), thickness)

            elif tool == TOOL_SQUARE and len(pts) > 1:
                # Force width and height to be equal based on largest distance
                dx = pts[1][0] - pts[0][0]
                dy = pts[1][1] - pts[0][1]
                side = max(abs(dx), abs(dy))
                new_x = pts[0][0] if dx > 0 else pts[0][0] - side
                new_y = pts[0][1] if dy > 0 else pts[0][1] - side
                pygame.draw.rect(screen, color, (new_x, new_y, side, side), thickness)

            elif tool == TOOL_CIRCLE and len(pts) > 1:
                dist = int(math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]))
                pygame.draw.circle(screen, color, pts[0], dist, thickness)

            elif tool == TOOL_RTRIANGLE and len(pts) > 1:
                # Right Triangle vertices: Start, MousePos, and a corner at (Start.x, MousePos.y)
                vertices = [pts[0], pts[1], (pts[0][0], pts[1][1])]
                pygame.draw.polygon(screen, color, vertices, thickness)

            elif tool == TOOL_ETRIANGLE and len(pts) > 1:
                # Calculate equilateral vertices using basic trigonometry (60 degrees)
                dx = pts[1][0] - pts[0][0]
                dy = pts[1][1] - pts[0][1]
                side = int(math.hypot(dx, dy))
                # Top vertex is start, calculate other two
                height = side * math.sqrt(3) / 2
                vertices = [
                    pts[0],
                    (pts[0][0] - side // 2, pts[0][1] + int(height)),
                    (pts[0][0] + side // 2, pts[0][1] + int(height))
                ]
                pygame.draw.polygon(screen, color, vertices, thickness)

            elif tool == TOOL_RHOMBUS and len(pts) > 1:
                # Four points: center-top, right-center, center-bottom, left-center
                x1, y1 = pts[0]
                x2, y2 = pts[1]
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                vertices = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
                pygame.draw.polygon(screen, color, vertices, thickness)

        pygame.display.flip()
        clock.tick(120)


def get_rect_tuple(p1, p2):
    x, y = min(p1[0], p2[0]), min(p1[1], p2[1])
    w, h = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    return (x, y, w, h)


def drawLineBetween(screen, start, end, width, color):
    dx, dy = start[0] - end[0], start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = i / iterations
        x = int((1 - progress) * start[0] + progress * end[0])
        y = int((1 - progress) * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


if __name__ == "__main__":
    main()