import pygame

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("mars_game/img/1sOI8h-removebg-preview (2).png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (300, 300))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.door_rect = pygame.Rect(self.x + 120, self.y + 230, 60, 70)
    def can_interact(self, player):
        player_rect = pygame.Rect(player.x + 40, player.y + 40, 80, 80)
        interact_rect = self.door_rect.inflate(120, 120)
        return player_rect.colliderect(interact_rect)
    
    def interact(self):
        pass


    def draw(self, screen, camera_x, camera_y):
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y
        screen.blit(self.img, (draw_x, draw_y))