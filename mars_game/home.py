import pygame

class Home:
    def __init__(self, x, y):
        self.x = 40
        self.y = 880
        self.img = pygame.image.load("mars_game/img/home.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (208, 126))  
        self.rect = pygame.Rect(self.x, self.y, 208, 126)    
        self.rover_rect = pygame.Rect(self.x, self.y, 228, 146)  
        
        self.door_rect = pygame.Rect(self.x, self.y, 150, 80)

    def can_interact(self, player):
        interact_zone = self.rect.inflate(80, 80)
        return interact_zone.colliderect(player.get_rect())

    def is_near_door(self, player):
        return self.door_rect.colliderect(player.get_rect())

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.img, (self.x - camera_x, self.y - camera_y))