import pygame

class Home:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("mars_game/img/home.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (380, 192))
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = pygame.Rect(self.x + 70, self.y, 220, 172)

        self.door_rect = pygame.Rect(470, 220, 100, 60)


    def can_interact(self, player):
        interact_zone = self.rect.inflate(80, 80)
        return interact_zone.colliderect(player.get_rect())

    def is_near_door(self, player):
        return self.door_rect.colliderect(player.get_rect())

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.img, (self.x - camera_x, self.y - camera_y))

