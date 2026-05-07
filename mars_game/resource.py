import pygame

class Resource:
    def __init__(self, x, y, name, image_path, size=(64, 64), pickup_time=1):
        self.x = x
        self.y = y
        self.name = name
        self.image_path = image_path
        self.size = size
        self.pickup_time = pickup_time

        self.img = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, size)

        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])

    def can_pickup(self, player):
        pickup_zone = self.rect.inflate(80, 80)
        return pickup_zone.colliderect(player.get_rect())
    def get_item_data(self):
        return {
            "name": self.name,
            "image": self.image_path
        }


    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.img, (self.x - camera_x, self.y - camera_y))
