import pygame
from player import Player

WIDTH, HEIGHT = 1024, 1024

def draw_infinite_map(screen, camera_x, camera_y, bg_top, bg_down):
    kartinki_w = bg_top.get_width()
    kartinki_h = bg_top.get_height()
    nomer_x_stolbka = (camera_x // kartinki_w) * kartinki_w - kartinki_w
    nomer_y_stolbka = (camera_y // kartinki_h) * kartinki_h - kartinki_h

    poziciya_y = nomer_y_stolbka
    while poziciya_y < camera_y + HEIGHT + kartinki_h:
        poziciya_x = nomer_x_stolbka
        while poziciya_x < camera_x + WIDTH + kartinki_w:
            if poziciya_y <= 0:
                screen.blit(bg_top, (poziciya_x - camera_x, poziciya_y - camera_y))
            else:
                screen.blit(bg_down, (poziciya_x - camera_x, poziciya_y - camera_y))
            poziciya_x += kartinki_w 
        poziciya_y += kartinki_h    
def main():
    pygame.init()
    WIDTH, HEIGHT = 1024, 1024
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player(WIDTH // 4, HEIGHT // 4)
    bg_top = pygame.image.load("mars_game/img/gemini-2.5-flash-image_pixel_art_mars_background_game_style_2D-0 (1) (6).png").convert()
    bg_down = pygame.image.load("mars_game/img/gemini-2.5-flash-image_pixel_art_mars_background_game_style_2D-0 (1) (5) (1).png").convert()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        player.handle_input()
        player.update(WIDTH, HEIGHT )
        camera_x = player.x - WIDTH // 2
        camera_y = player.y - HEIGHT // 2
        draw_infinite_map(screen, camera_x, camera_y, bg_top, bg_down)
        player.draw(screen, camera_x, camera_y)
        pygame.display.flip()


if __name__ == "__main__":
    main()

