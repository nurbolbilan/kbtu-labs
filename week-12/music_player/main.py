import pygame
from player import tracks, images, font_main, font_ui

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Music Player")

current_track = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                tracks[current_track].stop()
                tracks[current_track].play()
            elif event.key == pygame.K_s:
                for track in tracks:
                    track.stop()
            elif event.key == pygame.K_n:
                tracks[current_track].stop()
                current_track = (current_track + 1) % len(tracks)
                tracks[current_track].play()
            elif event.key == pygame.K_b:
                tracks[current_track].stop()
                current_track = (current_track - 1) % len(tracks)
                tracks[current_track].play()
            elif event.key == pygame.K_q:
                running = False

    screen.fill((25, 25, 25))
    screen.blit(images[current_track], (125, 80))

    if current_track % 2 == 0:
        text = "Gimme More"
        author = "Britney Spears"
        pos = (175, 350)
    else:
        text = "Again"
        author = "Noah Cyrus"
        pos = (200, 350)

    pos_text = font_main.render(text, True, (0, 255, 150))
    screen.blit(pos_text, pos)

    name_text = font_ui.render(author, True, (200, 200, 200))
    screen.blit(name_text, (180, 390))

    is_playing = "Now Playing..." if pygame.mixer.get_busy() else " Now stopped"
    status_color = (0, 255, 0) if pygame.mixer.get_busy() else (255, 50, 50)
    status_text = font_ui.render(is_playing, True, status_color)
    screen.blit(status_text, (175, 45))

    hint_text = font_ui.render("P: Play | S: Stop | N: Next | B: Back", True, (100, 100, 100))
    screen.blit(hint_text, (85, 450))

    pygame.display.update()

pygame.quit()