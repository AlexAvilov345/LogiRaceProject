import pygame

class GreenHouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.img = pygame.image.load("mars_game/img/greenhouse.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (444, 300))
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.rect = pygame.Rect(self.x, self.y - 10, self.width, self.height)
        self.door_rect = pygame.Rect(self.x + 110, self.y + 230, 80, 60)
        self.inside_door_rect = pygame.Rect(460, 850, 120, 80)

    def can_interact(self, player):
        interact_zone = self.door_rect.inflate(80, 80)
        return interact_zone.colliderect(player.get_rect())

    def is_near_door(self, player):
        return self.inside_door_rect.colliderect(player.get_rect())


    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.img, (self.x - camera_x, self.y - camera_y))

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            pygame.Rect(
                self.rect.x - camera_x,
                self.rect.y - camera_y,
                self.rect.width,
                self.rect.height
            ),
            3
        )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            pygame.Rect(
                self.door_rect.x - camera_x,
                self.door_rect.y - camera_y,
                self.door_rect.width,
                self.door_rect.height
            ),
            3
        )
