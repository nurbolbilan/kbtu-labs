import pygame
import datetime

def rotate_hand(surface, angle, center):
    rotated_surface = pygame.transform.rotate(surface, -angle)
    new_rect = rotated_surface.get_rect(center=center)
    return rotated_surface, new_rect

screen = pygame.display.set_mode((847, 847))
pygame.init()

mickey_image = pygame.image.load("images/mickeyclock.jpeg").convert_alpha()
right_hand = pygame.image.load("images/right_hand.png").convert_alpha()
left_hand = pygame.image.load("images/left_hand.png").convert_alpha()

clock = pygame.time.Clock()

running = True
while running:
    now = datetime.datetime.now()

    minutes_angle = now.minute * 6
    seconds_angle = now.second * 6

    screen.blit(mickey_image, (0, 0))

    surf_h, rect_h = rotate_hand(right_hand, minutes_angle, (427, 411))
    screen.blit(surf_h, rect_h)

    surf_m, rect_m = rotate_hand(left_hand, seconds_angle, (427, 411))
    screen.blit(surf_m, rect_m)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(30)

    pygame.display.update()