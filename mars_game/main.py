import pygame
from player import Player
from base import Base
from human import Human


WIDTH, HEIGHT = 1024, 1024
FPS = 60

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
    scene = "base"
    human = Human(500, 520)
    rover = Player(430, 520)
    camera_x = 0
    camera_y = 0


    active_player = human
    in_rover = False
    



    base = Base(300, 700)
    bases = [base]
    outside_player_x = base.x
    outside_player_y = base.y
    base_bg = pygame.image.load("mars_game/img/T_37CF.png").convert()
    base_bg = pygame.transform.scale(base_bg, (WIDTH, HEIGHT))
    base_walls = [
    pygame.Rect(100, 400, 840, 25),   
    pygame.Rect(100, 760, 840, 25),  
    pygame.Rect(100, 295, 25, 490),   
    pygame.Rect(915, 295, 25, 490),  
    
    pygame.Rect(685, 615, 165, 65),  
    pygame.Rect(685, 695, 165, 65), 
    pygame.Rect(850, 535, 80, 65),
    pygame.Rect(400, 370, 80, 115),   
    pygame.Rect(725, 370, 80, 115),
    pygame.Rect(280, 733, 165, 35),
    pygame.Rect(124, 543, 30, 115),
    pygame.Rect(212, 468, 50, 45),
    pygame.Rect(136, 467, 50, 50),
    pygame.Rect(851, 439, 50, 90),
]

    bg_top = pygame.image.load("mars_game/img/gemini-2.5-flash-image_pixel_art_mars_background_game_style_2D-0 (1) (6).png").convert()
    bg_down = pygame.image.load("mars_game/img/gemini-2.5-flash-image_pixel_art_mars_background_game_style_2D-0 (1) (5) (1).png").convert()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and scene == "mars":
                    if in_rover:
                        in_rover = False
                        active_player = human

                        human.x = rover.x + 120
                        human.y = rover.y
                        human.vel_x = 0
                        human.vel_y = 0
                        rover.vel_x = 0
                        rover.vel_y = 0

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_e and scene == "base":
                    if not in_rover:
                        if human.get_rect().colliderect(rover.get_rect().inflate(80, 80)):
                            in_rover = True
                            scene = "mars"
                            active_player = rover

                            rover.x = base.x + 120
                            rover.y = base.y + 330
                            rover.vel_x = 0
                            rover.vel_y = 0

                elif event.key == pygame.K_e and scene == "mars":
                    if not in_rover:
                        if human.get_rect().colliderect(rover.get_rect().inflate(120, 120)):
                            in_rover = True
                            active_player = rover

                            human.x = rover.x
                            human.y = rover.y
                            human.vel_x = 0
                            human.vel_y = 0

                    else:
                        for base in bases:
                            if base.can_interact(rover):
                                scene = "base"
                                in_rover = False
                                active_player = human

                                human.x = 500
                                human.y = 520
                                human.vel_x = 0
                                human.vel_y = 0

                                rover.x = 430
                                rover.y = 520
                                rover.vel_x = 0
                                rover.vel_y = 0




        
        if scene == "base":
            active_player.handle_input()
        elif scene == "mars":
            active_player.handle_input()
        active_player.animate()
        if active_player == human:
            human.animate()





        #if event.type == pygame.MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pos())

        





        if scene == "mars":
            if in_rover:
                rover.update(WIDTH, HEIGHT, bases)
                target_camera_x = active_player.x - WIDTH // 2
                target_camera_y = active_player.y - HEIGHT // 2

                camera_x += (target_camera_x - camera_x) * 0.08
                camera_y += (target_camera_y - camera_y) * 0.08

            else:
                human.update_mars(bases)
                target_camera_x = human.x - WIDTH // 2
                target_camera_y = human.y - HEIGHT // 2

                camera_x += (target_camera_x - camera_x) * 0.08
                camera_y += (target_camera_y - camera_y) * 0.08


            draw_infinite_map(screen, camera_x, camera_y, bg_top, bg_down)

            for base in bases:
                base.draw(screen, camera_x, camera_y)

            rover.draw(screen, camera_x, camera_y)
            if not in_rover:
                human.draw_mars(screen, camera_x, camera_y)


        elif scene == "base":
            active_player.update_inside_base(base_walls)
            screen.blit(base_bg, (0, 0))
    


            rover.draw(screen, 0, 0)

            if not in_rover:
                human.draw(screen, 0, 0)
        pygame.display.flip()


if __name__ == "__main__":
    main()

