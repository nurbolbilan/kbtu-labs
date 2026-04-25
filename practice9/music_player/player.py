import pygame

pygame.init()

tracks = [
    pygame.mixer.Sound('music/track1.mp3'),
    pygame.mixer.Sound('music/track2.mp3')
]

img1 = pygame.image.load('images/track1.jpg')
img1 = pygame.transform.scale(img1, (250, 250))

img2 = pygame.image.load('images/track2.jpg')
img2 = pygame.transform.scale(img2, (250, 250))

images = [img1, img2]

font_main = pygame.font.SysFont("Consolas", 28, bold=True)
font_ui = pygame.font.SysFont("Consolas", 18)