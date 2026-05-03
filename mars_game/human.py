import pygame


class Human:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 0.5
        self.size = 96

        self.frame_index = 0
        self.animation_speed = 0.08
        self.is_moving = False
        self.direction = "down"

        self.walk_down = self.load_frames([
            "mars_game/img/animate_img/1.png",
            "mars_game/img/animate_img/2.png",
            "mars_game/img/animate_img/3.png",
        ])

        self.walk_up = self.load_frames([
            "mars_game/img/animate_img/4.png",
            "mars_game/img/animate_img/5.png",
            "mars_game/img/animate_img/6.png",
        ])

        self.walk_left = self.load_frames([
            "mars_game/img/animate_img/10.png",
            "mars_game/img/animate_img/11.png",
            "mars_game/img/animate_img/12.png"
        ])

        self.walk_right = self.load_frames([
            "mars_game/img/animate_img/8.png",
            "mars_game/img/animate_img/7.png",
            "mars_game/img/animate_img/9.png",
        ])

        self.mars_down = pygame.image.load("mars_game/img/chpepper1squirePNG (6).png").convert_alpha()
        self.mars_down = pygame.transform.scale(self.mars_down, (self.size, self.size))

        self.mars_up = pygame.image.load("mars_game/img/chpepper1squirePNG (4) (1).png").convert_alpha()
        self.mars_up = pygame.transform.scale(self.mars_up, (self.size, self.size))

        self.mars_left = pygame.image.load("mars_game/img/chpepper1squirePNG (5) (1).png").convert_alpha()
        self.mars_left = pygame.transform.scale(self.mars_left, (self.size, self.size))

        self.mars_right = pygame.image.load("mars_game/img/chpepper1squirePNG (55).png").convert_alpha()
        self.mars_right = pygame.transform.scale(self.mars_right, (self.size, self.size))

        self.current_image = self.walk_down[0]
        self.current_mars_image = self.mars_down

        self.width = self.current_image.get_width()
        self.height = self.current_image.get_height()

    def load_frames(self, paths):
        frames = []

        for path in paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (self.size, self.size))
            frames.append(img)

        return frames

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.vel_x = 0
        self.vel_y = 0
        self.is_moving = False

        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.direction = "left"
            self.is_moving = True

        if keys[pygame.K_d]:
            self.vel_x = self.speed
            self.direction = "right"
            self.is_moving = True

        if keys[pygame.K_w]:
            self.vel_y = -self.speed
            self.direction = "up"
            self.is_moving = True

        if keys[pygame.K_s]:
            self.vel_y = self.speed
            self.direction = "down"
            self.is_moving = True

    def animate(self):
        if self.is_moving:
            self.frame_index += self.animation_speed
        else:
            self.frame_index = 0

        frames = {
            "down": self.walk_down,
            "up": self.walk_up,
            "left": self.walk_left,
            "right": self.walk_right,
        }

        mars_frames = {
            "down": self.mars_down,
            "up": self.mars_up,
            "left": self.mars_left,
            "right": self.mars_right,
        }

        current_frames = frames[self.direction]
        frame = int(self.frame_index) % len(current_frames)

        self.current_image = current_frames[frame]
        self.current_mars_image = mars_frames[self.direction]

    def get_rect(self):
        return pygame.Rect(self.x + 24, self.y + 24, 48, 48)

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

    def update_mars(self, bases):
        old_x = self.x
        old_y = self.y

        self.x += self.vel_x
        self.y += self.vel_y

        if self.y < 500:
            self.y = 500

        player_rect = self.get_rect()

        for base in bases:
            if player_rect.colliderect(base.rect):
                self.x = old_x
                self.y = old_y
                break

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.current_image, (self.x - camera_x, self.y - camera_y))

    def draw_mars(self, screen, camera_x, camera_y):
        screen.blit(self.current_mars_image, (self.x - camera_x, self.y - camera_y))
