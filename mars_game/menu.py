import pygame
import random

WIDTH, HEIGHT = 1024, 1024

UI_BG = (18, 20, 28)
UI_BORDER = (80, 180, 200)
UI_TEXT = (180, 240, 255)
UI_TEXT_DIM = (120, 150, 165)
UI_SELECTED = (255, 255, 255)
UI_SHADOW = (0, 0, 0)

fade_alpha = 0   
fade_speed = 8    
fade_state = "idle" 
fade_next = None    
class Dust:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.2, 0.8)
        self.size = random.randint(1, 3)

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)

    def draw(self, screen):
        pygame.draw.circle(screen, (200, 160, 120), (int(self.x), int(self.y)), self.size)
def fade_start(next_scene):
    global fade_alpha, fade_state, fade_next
    if fade_state == "idle":
        fade_next = next_scene
        fade_state = "out"
        fade_alpha = 0


def fade_update():
    global fade_alpha, fade_state
    result = None
    if fade_state == "out":
        fade_alpha += fade_speed
        if fade_alpha >= 255:
            fade_alpha = 255
            result = fade_next
            fade_state = "in"
    elif fade_state == "in":
        fade_alpha -= fade_speed
        if fade_alpha <= 0:
            fade_alpha = 0
            fade_state = "idle"
    return result


def fade_draw(screen):
    if fade_state != "idle":
        black = pygame.Surface((WIDTH, HEIGHT))
        black.fill((0, 0, 0))
        black.set_alpha(fade_alpha)
        screen.blit(black, (0, 0))


def fade_busy():
    return fade_state != "idle"


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen, font):
        color = (80, 120, 170) if self.rect.collidepoint(pygame.mouse.get_pos()) else (40, 50, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (180, 240, 255), self.rect, 3)
        surf = font.render(self.text, True, (255, 255, 255))
        screen.blit(surf, (
            self.rect.centerx - surf.get_width() // 2,
            self.rect.centery - surf.get_height() // 2
        ))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos())



class ToggleButton:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label

    def draw(self, screen, font, value):

        color = (55, 70, 95) if self.rect.collidepoint(pygame.mouse.get_pos()) else (40, 50, 70)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, UI_BORDER, self.rect, 3)


        label_surf = font.render(self.label, True, UI_TEXT)
        screen.blit(label_surf, (self.rect.x + 20, self.rect.centery - label_surf.get_height() // 2))

        val_text = "ON" if value else "OFF"
        val_color = (80, 220, 120) if value else (220, 80, 80)
        val_surf = font.render(val_text, True, val_color)
        screen.blit(val_surf, (
            self.rect.right - val_surf.get_width() - 20,
            self.rect.centery - val_surf.get_height() // 2
        ))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos())


class Menu:
    def __init__(self):
        self.bg = pygame.image.load("mars_game/img/menu1.jpg").convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        try:
            pygame.mixer.music.load("mars_game/sounds/respitemix.ogg")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  
        except:
            pass
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(40)
        overlay.fill((255, 80, 40)) 
        self.bg.blit(overlay, (0, 0))
        self.bg_x = 0
        self.dust = [Dust() for _ in range(80)]
        

        self.font       = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 22)
        self.font_small = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 14)
        self.font_tiny  = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 11)
        self.buttons = [
            Button(362, 350, 300, 70, "PLAY"),
            Button(362, 450, 300, 70, "SETTINGS"),
            Button(362, 550, 300, 70, "ABOUT"),
            Button(362, 650, 300, 70, "EXIT"),
        ]
        px = (WIDTH - 500) // 2
        py = (HEIGHT - 380) // 2
        self.toggle_fps   = ToggleButton(px + 30, py + 110, 440, 55, "SHOW FPS")
        self.toggle_sound = ToggleButton(px + 30, py + 185, 440, 55, "SOUND")
        self.btn_settings_back = Button(px + 100, py + 290, 300, 55, "BACK")
        self.btn_about_back = Button(362, 820, 300, 60, "BACK")

    def update(self):
        pass

    def _draw_bg(self, screen):
        screen.blit(self.bg, (self.bg_x, 0))
        screen.blit(self.bg, (self.bg_x + WIDTH, 0))

    def draw(self, screen):
        self._draw_bg(screen)
        title = self.font.render("MARS SURVIVAL", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        for btn in self.buttons:
            btn.draw(screen, self.font_small)
        fade_draw(screen)
        for d in self.dust:
            d.update()
            d.draw(screen)

    def draw_settings(self, screen, show_fps, sound_volume):
        self._draw_bg(screen)

        pw, ph = 500, 380
        px = (WIDTH - pw) // 2
        py = (HEIGHT - ph) // 2

        pygame.draw.rect(screen, (0, 0, 0), (px + 8, py + 8, pw, ph))
        pygame.draw.rect(screen, UI_BG,     (px, py, pw, ph))
        pygame.draw.rect(screen, UI_BORDER, (px, py, pw, ph), 5)

        title = self.font_small.render("SETTINGS", True, UI_TEXT)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, py + 35))

        self.toggle_fps.draw(screen, self.font_tiny, show_fps)
        self.toggle_sound.draw(screen, self.font_tiny, sound_volume > 0)
        self.btn_settings_back.draw(screen, self.font_small)
        fade_draw(screen)

    def draw_about(self, screen):
        self._draw_bg(screen)

        pw, ph = 680, 560
        px = (WIDTH - pw) // 2
        py = (HEIGHT - ph) // 2 - 30

        pygame.draw.rect(screen, (0, 0, 0), (px + 8, py + 8, pw, ph))
        pygame.draw.rect(screen, UI_BG,     (px, py, pw, ph))
        pygame.draw.rect(screen, UI_BORDER, (px, py, pw, ph), 5)

        title = self.font.render("ABOUT", True, UI_TEXT)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, py + 30))

        lines = [
            ("MARS SURVIVAL",                    UI_TEXT,     self.font_small),
            ("",                                 None,        None),
            ("Survive on the red planet.",        UI_TEXT_DIM, self.font_tiny),
            ("Collect resources, build your base",UI_TEXT_DIM, self.font_tiny),
            ("and grow food to stay alive.",      UI_TEXT_DIM, self.font_tiny),
            ("",                                 None,        None),
            ("CONTROLS:",                         UI_BORDER,   self.font_small),
            ("WASD  -  Move",            UI_TEXT_DIM, self.font_tiny),
            ("E  -  Interact",                    UI_TEXT_DIM, self.font_tiny),
            ("Q  -  Exit rover",                  UI_TEXT_DIM, self.font_tiny),
            ("TAB  -  Inventory",                 UI_TEXT_DIM, self.font_tiny),
            ("",                                 None,        None),
            ("MUSIC BY Trevor Lentz",             UI_TEXT_DIM, self.font_tiny),
            ("Version 1.0",                       UI_TEXT_DIM, self.font_tiny),
        ]

        y = py + 95
        for text, color, font in lines:
            if not text or font is None:
                y += 18
                continue
            surf = font.render(text, True, color)
            screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
            y += surf.get_height() + 10

        self.btn_about_back.draw(screen, self.font_small)
        fade_draw(screen)

    def handle_event(self, event):
        if fade_busy():
            return None
        for btn in self.buttons:
            if btn.is_clicked(event):
                return btn.text
        return None

    def handle_settings_event(self, event, show_fps, sound_volume):
        if fade_busy():
            return show_fps, sound_volume

        if self.toggle_fps.is_clicked(event):
            show_fps = not show_fps

        elif self.toggle_sound.is_clicked(event):
            sound_volume = 0.0 if sound_volume > 0 else 1.0
            try:
                pygame.mixer.music.set_volume(sound_volume)
            except Exception:
                pass

        elif self.btn_settings_back.is_clicked(event):
            fade_start("menu")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            fade_start("menu")

        return show_fps, sound_volume

    def handle_about_event(self, event):
        if fade_busy():
            return
        if self.btn_about_back.is_clicked(event):
            fade_start("menu")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            fade_start("menu")

    def update_fade(self):
        return fade_update()