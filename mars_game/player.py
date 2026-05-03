import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.acceleration = 0.03
        self.vel_x = 0
        self.vel_y = 0
        

        self.img_right = pygame.image.load("mars_game/img/rover.1x.thumb (1).png").convert_alpha()
        self.img_right = pygame.transform.scale(self.img_right, (160, 160))
        
        self.img_left = pygame.image.load("mars_game/img/rover.1x.thumb (3).png").convert_alpha()
        self.img_left = pygame.transform.scale(self.img_left, (160, 160))

        self.img_up = pygame.image.load("mars_game/img/gemini-2.5-flash-image_2D_pixel_art_rover_on_Mars_top-down_RPG_style_like_Undertale_the_rover_is_facing-0 (1).png").convert_alpha()
        self.img_up = pygame.transform.scale(self.img_up, (220, 220))
        
        self.img_down = pygame.image.load("mars_game/img/gemini-2.5-flash-image_2D_pixel_art_rover_on_Mars_top-down_RPG_style_like_Undertale_the_rover_is_facing-0 (2).png").convert_alpha()
        self.img_down = pygame.transform.scale(self.img_down, (220, 220))

        self.current_image = self.img_right
    
        self.width = self.current_image.get_width()
        self.height = self.current_image.get_height()
        

    def handle_input(self):
        keys = pygame.key.get_pressed()
        target_x = 0
        target_y = 0

        if keys[pygame.K_a]: # Влево
            target_x = -self.speed
            self.current_image = self.img_left
        elif keys[pygame.K_d]: # Вправо
            target_x = self.speed
            self.current_image = self.img_right
        
        if keys[pygame.K_w]: # Вверх
            target_y = -self.speed
            self.current_image = self.img_up
        elif keys[pygame.K_s]: # Вниз
            target_y = self.speed
            self.current_image = self.img_down


        self.vel_x += (target_x - self.vel_x) * self.acceleration
        self.vel_y += (target_y - self.vel_y) * self.acceleration

    def update(self, screen_width, screen_height, bases):
        old_x = self.x
        old_y = self.y
        self.x += self.vel_x
        self.y += self.vel_y
       
        if self.y < 500:
            self.y = 500
        player_rect = pygame.Rect(self.x + 40, self.y + 40, 80, 80)
        for base in bases:
            if player_rect.colliderect(base.rect):
                self.x = old_x
                self.y = old_y
                break
    def update_inside_base(self, walls):
        old_x = self.x
        old_y = self.y

        self.x += self.vel_x
        self.y += self.vel_y

        player_rect = self.get_rect()


        for wall in walls:
            if player_rect.colliderect(wall):
                self.x = old_x
                self.y = old_y
                break
    def get_rect(self):
        return pygame.Rect(self.x + 40, self.y + 40, 80, 80)

        

    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        screen.blit(self.current_image, (draw_x, draw_y))