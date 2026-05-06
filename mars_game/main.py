import pygame
from player import Player
from base import Base
from human import Human
from home import Home
from greenhouse import GreenHouse


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
    clock = pygame.time.Clock()
    scene = "base"
    human = Human(500, 520)
    rover = Player(430, 520)
    camera_x = 0
    camera_y = 0


    active_player = human
    in_rover = False
    



    base = Base(300, 700)
    bases = [base]
    home = Home(50, 990)   
    homes = [home]
    home_bg = pygame.image.load("mars_game/img/home_inside.png").convert()
    home_bg = pygame.transform.scale(home_bg, (WIDTH, HEIGHT))

    home_walls = [
    pygame.Rect(100, 210, 800, 20),  
    pygame.Rect(100, 920, 800, 20),
    pygame.Rect(100, 100, 20, 800),
    pygame.Rect(900, 100, 20, 800),

    pygame.Rect(125, 232, 70, 50),  
    pygame.Rect(122, 872, 40, 50),
    pygame.Rect(833, 232, 70, 50),
    pygame.Rect(859, 883, 70, 50),

    pygame.Rect(658, 235, 90, 90),
    pygame.Rect(792, 377, 60, 160),

    pygame.Rect(143, 424, 160, 110),

    pygame.Rect(120, 560, 110, 110),

    pygame.Rect(134, 690, 160, 110),
    pygame.Rect(645, 536, 120, 140),
    pygame.Rect(790, 580, 75, 80),

    pygame.Rect(805, 698, 100, 160),
]
    greenhouse = GreenHouse(630, 840)
    greenhouses = [greenhouse]

    greenhouse_bg = pygame.image.load("mars_game/img/greenhouse_bg.png").convert()
    greenhouse_bg = pygame.transform.scale(greenhouse_bg, (WIDTH, HEIGHT))

    greenhouse_walls = [
    pygame.Rect(75, 333, 870, 25),   
    pygame.Rect(150, 813, 430, 25),  
    pygame.Rect(65, 95, 25, 670),     
    pygame.Rect(950, 95, 25, 670),  
    pygame.Rect(80, 303, 180, 130), 


    pygame.Rect(83, 528, 110, 100),
    pygame.Rect(64, 737, 100, 25), 
    pygame.Rect(253, 737, 200, 25), 
    pygame.Rect(470, 260, 490, 100), 


    pygame.Rect(426, 390, 490, 30),
    pygame.Rect(431, 652, 490, 110)
]

    outside_player_x = base.x
    outside_player_y = base.y
    base_bg = pygame.image.load("mars_game/img/base.png").convert()
    base_bg = pygame.transform.scale(base_bg, (WIDTH, HEIGHT))
    base_walls = [
    pygame.Rect(95, 240, 840, 20),  #веохняя 
    pygame.Rect(95, 920, 840, 20),  #нижня
    pygame.Rect(140, 95, 20, 820),  #левая 
    pygame.Rect(860, 95, 20, 820),  #правая 

    pygame.Rect(105, 880, 305, 20),   
    pygame.Rect(610, 880, 295, 20), 

    pygame.Rect(760, 115, 140, 200),


    pygame.Rect(115, 320, 155, 220),

    pygame.Rect(750, 330, 155, 220),

    pygame.Rect(150, 590, 90, 70),

    pygame.Rect(720, 590, 155, 130),

    pygame.Rect(140, 735, 200, 120),
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
                        human.x = rover.x + 130
                        human.y = rover.y + 40
                        human.vel_x = 0
                        human.vel_y = 0
                        rover.vel_x = 0
                        rover.vel_y = 0

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
                            for h in homes:
                                if h.can_interact(human):
                                    scene = "home"
                                    human.x = 500
                                    human.y = 500
                                    human.vel_x = 0
                                    human.vel_y = 0
                                for g in greenhouses:
                                    if g.can_interact(human):
                                        scene = "greenhouse"
                                        human.x = 500
                                        human.y = 500
                                        human.vel_x = 0
                                        human.vel_y = 0

                    else:
                        for base in bases:
                            if base.can_interact(rover):
                                scene = "base"
                                in_rover = False
                                active_player = human

                                human.x = 600
                                human.y = 520
                                human.vel_x = 0
                                human.vel_y = 0

                                rover.x = 430
                                rover.y = 520
                                rover.vel_x = 0
                                rover.vel_y = 0     
                elif event.key == pygame.K_e and scene == "home":
                    if home.is_near_door(human):
                        scene = "mars"
                        human.x = home.x + 140
                        human.y = home.y + 200
                        human.vel_x = 0
                        human.vel_y = 0
                elif event.key == pygame.K_e and scene == "greenhouse":
                    if greenhouse.is_near_door(human):
                        scene = "mars"
                        human.x = greenhouse.x + 140
                        human.y = greenhouse.y + 300
                        human.vel_x = 0
                        human.vel_y = 0

        if active_player == human:
            if scene == "base":
                human.speed = human.base_speed
        elif scene == "mars":
            human.speed = human.mars_speed

        active_player.handle_input()


        if active_player == human:
            human.animate()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        
        if scene == "mars":
            buildings = homes + greenhouses
            if in_rover:              
                rover.update(WIDTH, HEIGHT, bases, buildings)
                target_camera_x = active_player.x - WIDTH // 2
                target_camera_y = active_player.y - HEIGHT // 2

                camera_x += (target_camera_x - camera_x) * 0.08
                camera_y += (target_camera_y - camera_y) * 0.08

            else:
                human.update_mars(bases,rover, buildings)
                target_camera_x = human.x - WIDTH // 2
                target_camera_y = human.y - HEIGHT // 2

                camera_x += (target_camera_x - camera_x) * 0.08
                camera_y += (target_camera_y - camera_y) * 0.08


            draw_infinite_map(screen, camera_x, camera_y, bg_top, bg_down)

            for base in bases:
                base.draw(screen, camera_x, camera_y)
            for h in homes:
                h.draw(screen, camera_x, camera_y)
            for g in greenhouses:
                g.draw(screen, camera_x, camera_y)


            rover.draw(screen, camera_x, camera_y)
            if not in_rover:
                human.draw_mars(screen, camera_x, camera_y)


        elif scene == "base":
            if active_player == human:
                human.update_inside_base(base_walls, rover)
            else:
                active_player.update_inside_base(base_walls)
            screen.blit(base_bg, (0, 0))
            rover.draw(screen, 0, 0)       
            if not in_rover:
                human.draw(screen, 0, 0)     

        elif scene == "home":
            human.update_inside_base(home_walls)
            screen.blit(home_bg, (0, 0))
            human.draw(screen, 0, 0)

            #for wall in base_walls:
                #pygame.draw.rect(screen, (255, 0, 0), wall, 2)
        elif scene == "greenhouse":
            human.update_inside_base(greenhouse_walls)
            screen.blit(greenhouse_bg, (0, 0))
            human.draw(screen, 0, 0)

            #for wall in greenhouse_walls:
                #pygame.draw.rect(screen, (255, 0, 0), wall, 2)


            rover.draw(screen, 0, 0)

            if not in_rover:
                human.draw(screen, 0, 0)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

