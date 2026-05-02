import pygame


class Button:
    def __init__(self, x, y, width, height, text,
                 color=(70, 130, 180), hover_color=None,
                 text_color=(255, 255, 255), font_size=22):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or tuple(min(c + 40, 255) for c in color)
        self.text_color = text_color
        self.font = pygame.font.SysFont("Verdana", font_size, bold=True)
        self.hovered = False

    def draw(self, screen):
        col = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, col, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)
        surf = self.font.render(self.text, True, self.text_color)
        screen.blit(surf, surf.get_rect(center=self.rect.center))

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class TextInput:
    def __init__(self, x, y, width, height,
                 placeholder="Enter name...", max_length=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.font = pygame.font.SysFont("Verdana", 22)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=6)
        pygame.draw.rect(screen, (70, 130, 180), self.rect, 2, border_radius=6)
        if self.text:
            surf = self.font.render(self.text, True, (0, 0, 0))
        else:
            surf = self.font.render(self.placeholder, True, (160, 160, 160))
        screen.blit(surf, (self.rect.x + 10, self.rect.y + 9))

    def get_text(self):
        return self.text.strip() or "Player"