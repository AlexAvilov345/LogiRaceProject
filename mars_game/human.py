import pygame


class Human:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.base_speed = 4.5
        self.mars_speed = 5
        self.speed = self.base_speed
        self.size = 80
        self.max_hp = 5
        self.hp = 5

        self.frame_index = 0
        self.animation_speed = 0.12
        self.is_moving = False
        self.direction = "down"

        self.walk_down = self.load_frames([
            "mars_game/img/anim_img/human1.png",
            "mars_game/img/anim_img/human2.png",
            "mars_game/img/anim_img/human3.png",
            "mars_game/img/anim_img/human4.png",
        ])

        self.walk_up = self.load_frames([
            "mars_game/img/anim_img/human13.png",
            "mars_game/img/anim_img/human14.png",
            "mars_game/img/anim_img/human15.png",
            "mars_game/img/anim_img/human16.png",
        ])

        self.walk_left = self.load_frames([
            "mars_game/img/anim_img/human5.png",
            "mars_game/img/anim_img/human6.png",
            "mars_game/img/anim_img/human7.png",
            "mars_game/img/anim_img/human8.png",
        ])

        self.walk_right = self.load_frames([
            
            "mars_game/img/anim_img/human9.png",
            "mars_game/img/anim_img/human10.png",
            "mars_game/img/anim_img/human11.png",
            "mars_game/img/anim_img/human12.png",
        ])

        

        self.mars_walk_down = self.load_frames([
            "mars_game/img/anim2_img/astronaut1.png",
            "mars_game/img/anim2_img/astronaut2.png",
            "mars_game/img/anim2_img/astronaut3.png",
            "mars_game/img/anim2_img/astronaut4.png",
        ])


        self.mars_walk_up = self.load_frames([
            "mars_game/img/anim2_img/astronaut13.png",
            "mars_game/img/anim2_img/astronaut14.png",
            "mars_game/img/anim2_img/astronaut15.png",
            "mars_game/img/anim2_img/astronaut16.png",
        ])

        self.mars_walk_left = self.load_frames([
            "mars_game/img/anim2_img/astronaut5.png",
            "mars_game/img/anim2_img/astronaut6.png",
            "mars_game/img/anim2_img/astronaut7.png",
            "mars_game/img/anim2_img/astronaut8.png",
        ])

        self.mars_walk_right = self.load_frames([
            "mars_game/img/anim2_img/astronaut9.png",
            "mars_game/img/anim2_img/astronaut10.png",
            "mars_game/img/anim2_img/astronaut11.png",
            "mars_game/img/anim2_img/astronaut12.png",
        ])


        self.current_image = self.walk_down[0]
        self.current_mars_image = self.mars_walk_down

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
            "down":  self.walk_down,
            "up":    self.walk_up,
            "left":  self.walk_left,
            "right": self.walk_right,
        }

        mars_frames = {
            "down":  self.mars_walk_down,
            "up":    self.mars_walk_up,
            "left":  self.mars_walk_left,
            "right": self.mars_walk_right,
        }

        frame = int(self.frame_index) % 4

        self.current_image      = frames[self.direction][frame]
        self.current_mars_image = mars_frames[self.direction][frame]

    def get_rect(self):
        return pygame.Rect(self.x , self.y + 24, 88, 60)
    

    def update_inside_base(self, walls, rover=None):
        self.x += self.vel_x

        for wall in walls:
            if self.get_rect().colliderect(wall):
                self.x -= self.vel_x
                break

        if rover is not None and self.get_rect().colliderect(rover.get_rect()):
            self.x -= self.vel_x

        self.y += self.vel_y

        for wall in walls:
            if self.get_rect().colliderect(wall):
                self.y -= self.vel_y
                break

        if rover is not None and self.get_rect().colliderect(rover.get_rect()):
            self.y -= self.vel_y

    def update_mars(self, bases, rover, homes=None):
        self.x += self.vel_x

        for base in bases:
            if self.get_rect().colliderect(base.rect):
                self.x -= self.vel_x
                break

        if homes:
            for h in homes:
                if self.get_rect().colliderect(h.rect):
                    self.x -= self.vel_x
                    break

        if rover is not None and self.get_rect().colliderect(rover.get_rect()):
            self.x -= self.vel_x    


        self.y += self.vel_y

        if self.y < 500:
            self.y = 500

        for base in bases:
            if self.get_rect().colliderect(base.rect):
                self.y -= self.vel_y
                break

        if homes:
            for h in homes:
                if self.get_rect().colliderect(h.rect):
                    self.y -= self.vel_y
                    break

        if rover is not None and self.get_rect().colliderect(rover.get_rect()):
                self.y -= self.vel_y



    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.current_image, (self.x - camera_x, self.y - camera_y))

    def draw_mars(self, screen, camera_x, camera_y):
        screen.blit(self.current_mars_image, (self.x - camera_x, self.y - camera_y))

