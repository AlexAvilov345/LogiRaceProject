import pygame
import random
from player import Player
from base import Base
from human import Human
from home import Home
from greenhouse import GreenHouse
from resource import Resource
from menu import Menu, fade_start, fade_update, fade_busy, fade_draw



WIDTH, HEIGHT = 1024, 1024
FPS = 60
UI_BG = (18, 20, 28)
UI_SHADOW = (0, 0, 0)
UI_BORDER = (80, 180, 200)
UI_SLOT = (30, 34, 44)
UI_SLOT_BORDER = (80, 180, 200)
UI_TEXT = (180, 240, 255)
UI_TEXT_DIM = (120, 150, 165)
UI_SELECTED = (255, 255, 255)



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
class MapObject:
    def __init__(self, x, y, image_path, size, rect_offset):
        self.x = x
        self.y = y
        self.img = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, size)

        offset_x, offset_y, rect_w, rect_h = rect_offset
        self.rect = pygame.Rect(self.x + offset_x, self.y + offset_y, rect_w, rect_h)

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.img, (self.x - camera_x, self.y - camera_y))
def spawn_resources(resource_types, count, blocked_objects):
    resources = []

    for i in range(count):
        while True:
            x = random.randint(-1500, 2500)
            y = random.randint(550, 2500)

            resource_data = random.choices(resource_types, weights=[r["shans"] for r in resource_types], k=1 )[0]

            resource = Resource(
                x,
                y,
                resource_data["name"],
                resource_data["image"],
                resource_data["size"],
                resource_data["pickup_time"]
            )

            can_spawn = True

            for obj in blocked_objects:
                if resource.rect.colliderect(obj.rect.inflate(100, 100)):
                    can_spawn = False
                    break

            if can_spawn:
                resources.append(resource)
                break

    return resources

def draw_inventory(screen, inventory):
    panel_width = 560
    panel_height = 420
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2
    shadow_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 100), (0, 0, panel_width, panel_height))
    screen.blit(shadow_surf, (panel_x + 12, panel_y + 12)) 

    pygame.draw.rect(screen, UI_BG, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BORDER, (panel_x, panel_y, panel_width, panel_height), 6)



    font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)
    title = font.render("INVENTORY", True, UI_TEXT)
    screen.blit(title, (panel_x + 195, panel_y + 25))
    slot_size = 72
    item_size = 48
    gap = 14
    columns = 6
    start_x = panel_x + 30
    start_y = panel_y + 70

    for i in range(24):
        row = i // columns
        col = i % columns
        slot_x = start_x + col * (slot_size + gap)
        slot_y = start_y + row * (slot_size + gap)

        pygame.draw.rect(screen, UI_SLOT, (slot_x, slot_y, slot_size, slot_size))
        pygame.draw.rect(screen, UI_SLOT_BORDER, (slot_x, slot_y, slot_size, slot_size), 4)
        pygame.draw.rect(screen, UI_SHADOW, (slot_x + 6, slot_y + 6, slot_size - 12, slot_size - 12), 2)

        if i < len(inventory):
            item = inventory[i]
            item_img = pygame.image.load(item["image"]).convert_alpha()
            item_img = pygame.transform.scale(item_img, (item_size, item_size))

            item_x = slot_x + (slot_size - item_size) // 2
            item_y = slot_y + (slot_size - item_size) // 2
            screen.blit(item_img, (item_x, item_y))

def draw_pickup_bar(screen, resource, progress, camera_x, camera_y):
    bar_width = 70
    bar_height = 10

    x = resource.x + resource.size[0] // 2 - bar_width // 2 - camera_x
    y = resource.y - 18 - camera_y

    percent = progress / resource.pickup_time
    if percent > 1:
        percent = 1

    pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, bar_width + 4, bar_height + 4))
    pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, (80, 220, 90), (x, y, bar_width * percent, bar_height))
def draw_storage_window(screen, inventory, storage_inventory, storage_side, selected_slot):
    panel_width = 760
    panel_height = 420
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    pygame.draw.rect(screen, UI_SHADOW, (panel_x + 10, panel_y + 10, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BG, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BORDER, (panel_x, panel_y, panel_width, panel_height), 6)


    font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)

    left_title = font.render("PLAYER", True, UI_TEXT)
    right_title = font.render("STORAGE", True, UI_TEXT)


    screen.blit(left_title, (panel_x + 115, panel_y + 25))
    screen.blit(right_title, (panel_x + 500, panel_y + 25))

    draw_item_grid(screen, inventory, panel_x + 55, panel_y + 80, storage_side == "player", selected_slot)
    draw_item_grid(screen, storage_inventory, panel_x + 435, panel_y + 80, storage_side == "storage", selected_slot)


def draw_item_grid(screen, items, start_x, start_y, active, selected_slot):
    slot_size = 64
    item_size = 44
    gap = 12
    columns = 3
    total_slots = 12

    for i in range(total_slots):
        row = i // columns
        col = i % columns

        x = start_x + col * (slot_size + gap)
        y = start_y + row * (slot_size + gap)

        pygame.draw.rect(screen, UI_SLOT, (x, y, slot_size, slot_size))
        pygame.draw.rect(screen, UI_SLOT_BORDER, (x, y, slot_size, slot_size), 4)


        if active and i == selected_slot:
            pygame.draw.rect(screen, UI_SELECTED, (x - 3, y - 3, slot_size + 6, slot_size + 6), 3)


        if i < len(items):
            item = items[i]
            item_img = pygame.image.load(item["image"]).convert_alpha()
            item_img = pygame.transform.scale(item_img, (item_size, item_size))

            item_x = x + (slot_size - item_size) // 2
            item_y = y + (slot_size - item_size) // 2
            screen.blit(item_img, (item_x, item_y))


def draw_computer_menu(screen, computer_menu, computer_selected, inventory=None, storage_inventory=None):
    if inventory is None:
        inventory = []
    if storage_inventory is None:
        storage_inventory = []

    panel_width = 620
    panel_height = 430
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    pygame.draw.rect(screen, UI_SHADOW, (panel_x + 10, panel_y + 10, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BG, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BORDER, (panel_x, panel_y, panel_width, panel_height), 5)


    font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)
    title = font.render("BASE COMPUTER", True, UI_TEXT)
    screen.blit(title, (panel_x + 200, panel_y + 35))
    if computer_menu == "process":
        all_items = inventory + storage_inventory

        process_title = font.render("PROCESS RESOURCES", True, UI_TEXT)
        screen.blit(process_title, (panel_x + 50, panel_y + 90))

        slot_size = 64
        item_size = 44
        gap = 14
        columns = 5

        start_x = panel_x + 80
        start_y = panel_y + 145

        if len(all_items) == 0:
            text = font.render("NO RESOURCES", True, UI_TEXT_DIM)
            screen.blit(text, (panel_x + 200, panel_y + 210))
            return

        for i, item in enumerate(all_items[:15]):
            row = i // columns
            col = i % columns

            x = start_x + col * (slot_size + gap)
            y = start_y + row * (slot_size + gap)

            pygame.draw.rect(screen, UI_SLOT, (x, y, slot_size, slot_size))
            pygame.draw.rect(screen, UI_SLOT_BORDER, (x, y, slot_size, slot_size), 4)

            if i == computer_selected:
                pygame.draw.rect(screen, UI_SELECTED, (x - 3, y - 3, slot_size + 6, slot_size + 6), 3)

            item_img = pygame.image.load(item["image"]).convert_alpha()
            item_img = pygame.transform.scale(item_img, (item_size, item_size))
            screen.blit(item_img, (x + 10, y + 10))

        return
    if computer_menu == "main":
        options = ["PLAYER UPGRADES", "ROVER UPGRADES", "BASE UPGRADES", "PROCESS RESOURCES"]
    elif computer_menu == "player":
        options = ["ARMOR", "HP", "SPEED"]
    elif computer_menu == "rover":
        options = ["SPEED", "ARMOR", "BATTERY"]
    elif computer_menu == "base":
        options = ["STORAGE", "ARMOR", "ENERGY"]
    elif computer_menu == "process":
        current_options_count = max(1, len(inventory) + len(storage_inventory))

    else:
        options = []

    start_y = panel_y + 110

    for i, option in enumerate(options):
        y = start_y + i * 55

        if i == computer_selected:
            pygame.draw.rect(screen, UI_SELECTED, (panel_x + 55, y - 12, panel_width - 110, 38), 3)
            color = UI_SELECTED

        else:
            color = UI_TEXT_DIM


        text = font.render(option, True, color)
        screen.blit(text, (panel_x + 80, y))

def draw_home_computer(screen, home_info_selected, rover_inside_base, inventory, storage_inventory, resources):
    panel_width = 680
    panel_height = 430
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    pygame.draw.rect(screen, UI_SHADOW, (panel_x + 10, panel_y + 10, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BG, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BORDER, (panel_x, panel_y, panel_width, panel_height), 5)

    font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)
    small_font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 13)

    title = font.render("HOME COMPUTER", True, UI_TEXT)
    screen.blit(title, (panel_x + 220, panel_y + 35))

    tabs = ["BASE", "HOME", "GREENHOUSE", "ROVER"]

    for i, tab in enumerate(tabs):
        x = panel_x + 45 + i * 150
        y = panel_y + 90

        if i == home_info_selected:
            pygame.draw.rect(screen, UI_SELECTED, (x - 10, y - 10, 145, 34), 3)
            color = UI_SELECTED
        else:
            color = UI_TEXT_DIM

        text = small_font.render(tab, True, color)
        screen.blit(text, (x, y))

    info_y = panel_y + 165

    if home_info_selected == 0:
        lines = [
            "BASE STATUS: ONLINE",
            f"STORAGE: {len(storage_inventory)} / 12",
            f"INVENTORY: {len(inventory)} / 24",
        ]

    elif home_info_selected == 1:
        lines = [
            "HOME STATUS: ONLINE",
            "OXYGEN: NORMAL",
            "ENERGY: NORMAL",
        ]

    elif home_info_selected == 2:
        lines = [
            "GREENHOUSE STATUS: ONLINE",
            "PLANTS: STABLE",
            "WATER: NORMAL",
        ]

    else:
        if rover_inside_base:
            rover_place = "IN BASE"
        else:
            rover_place = "ON MARS"

        lines = [
            "ROVER STATUS: ONLINE",
            f"LOCATION: {rover_place}",
            f"MARS RESOURCES: {len(resources)}",
        ]

    for i, line in enumerate(lines):
        text = small_font.render(line, True, UI_TEXT)
        screen.blit(text, (panel_x + 90, info_y + i * 45))
def draw_greenhouse_menu(
    screen,
    greenhouse_selected,
    crop_recipes,
    growing_crop,
    growing_timer,
    growing_ready
):
    panel_width = 620
    panel_height = 420

    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2

    pygame.draw.rect(screen, UI_SHADOW, (panel_x + 10, panel_y + 10, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BG, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, UI_BORDER, (panel_x, panel_y, panel_width, panel_height), 5)

    font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)

    title = font.render("GREENHOUSE COMPUTER", True, UI_TEXT)
    screen.blit(title, (panel_x + 150, panel_y + 35))

    recipe_keys = list(crop_recipes.keys())

    for i, key in enumerate(recipe_keys):
        recipe = crop_recipes[key]

        y = panel_y + 120 + i * 60

        color = UI_TEXT_DIM

        if i == greenhouse_selected:
            color = UI_SELECTED

            pygame.draw.rect(
                screen,
                UI_SELECTED,
                (panel_x + 40, y - 10, 520, 38),
                3
            )

        text = font.render(
            f"{recipe['title']} - {recipe['cost']} DETAILS",
            True,
            color
        )

        screen.blit(text, (panel_x + 70, y))

    if growing_crop is not None:
        recipe = crop_recipes[growing_crop]

        if growing_ready:
            status = f"{recipe['title']} READY!"
        else:
            seconds = max(0, growing_timer // FPS)
            status = f"GROWING: {seconds} SEC"

        status_text = font.render(status, True, UI_TEXT)

        screen.blit(status_text, (panel_x + 190, panel_y + 340))
def count_item(items, name):
    count = 0
    for item in items:
        if item["name"] == name:
            count += 1
    return count

def remove_details(inventory, storage_inventory, amount):
    removed = 0
    for items in [inventory, storage_inventory]:
        i = 0

        while i < len(items):
            if items[i]["name"] == "detail":
                items.pop(i)
                removed += 1
                if removed >= amount:
                    return True
            else:
                i += 1

    return False

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    scene = "menu"
    menu = Menu()
    human = Human(500, 400)
    rover = Player(430, 520)
    camera_x = 0
    camera_y = 0



    active_player = human
    in_rover = False
    rover_inside_base = True
    vishka = MapObject(
        650,
        600,
        "mars_game/img/vishka.png",
        (200, 200),
        (70, 40, 60, 100)
    )
    map_objects = [vishka]
    
    base = Base(300, 700)
    bases = [base]
    home = Home(-30, 900)   
    homes = [home]
    home_bg = pygame.image.load("mars_game/img/home_inside.png").convert()
    home_bg = pygame.transform.scale(home_bg, (WIDTH, HEIGHT))
    



    home_walls = [
        pygame.Rect(100, 210, 800, 20),  
        pygame.Rect(100, 940, 800, 20),
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
        pygame.Rect(75, 350, 870, 25),   
        pygame.Rect(150, 813, 430, 25),  
        pygame.Rect(65, 95, 25, 670),     
        pygame.Rect(950, 95, 25, 670),  

        pygame.Rect(80, 303, 180, 130), 

        pygame.Rect(83, 528, 90, 100),
        pygame.Rect(64, 737, 80, 25), 
        pygame.Rect(253, 737, 200, 25), 
        pygame.Rect(470, 260, 490, 100), 


        pygame.Rect(426, 410, 490, 30),
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




    

    inventory = []
    show_inventory = False
    pickup_resource = None
    pickup_progress = 0
    storage_inventory = []
    show_storage = False
    storage_side = "player"  
    selected_slot = 0
    storage_rect = pygame.Rect(184, 136, 155, 130)  
    locked_storage_rect = pygame.Rect(352, 136, 155, 130)
    locked_message_timer = 0
    storage_full_timer = 0
    locked_storage_rect2 = pygame.Rect(514, 136, 155, 130)

    computer_rect = pygame.Rect(190, 588, 60, 80)
    show_computer = False
    computer_menu = "main"
    computer_selected = 0
    home_computer_rect = pygame.Rect(326, 179, 90, 90)
    show_home_computer = False
    home_info_selected = 0

    greenhouse_computer_rect = pygame.Rect(296, 315, 60, 80)
    show_greenhouse_menu = False
    greenhouse_selected = 0
    growing_crop = None
    growing_timer = 0
    growing_ready = False

    show_fps = False
    sound_volume = 50




    base_exit_rect = pygame.Rect(411, 895, 160, 60)

    resource_types = [
        {
            "name": "mars_stone",
            "image": "mars_game/img/resurs1.png",
            "size": (64, 64),
            "shans": 85,
            "pickup_time": 1
        },
        {
            "name": "big_mars_stone",
            "image": "mars_game/img/resurs(2).png",
            "size": (160, 160),
            "shans": 20,
            "pickup_time": 3
        },
    ]

    detail_item = {
        "name": "detail",
        "image": "mars_game/img/detail1 (1).png"
    }
    crop_recipes = {
        "potato": {
            "title": "POTATO",
            "cost": 1,
            "time": 5 * FPS,
            "item": {"name": "potato", "image": "mars_game/img/potato.png"}
        },
        "corn": {
            "title": "CORN",
            "cost": 2,
            "time": 8 * FPS,
            "item": {"name": "corn", "image": "mars_game/img/corn.png"}
        },
        "carrot": {
            "title": "CARROT",
            "cost": 1,
            "time": 6 * FPS,
            "item": {"name": "carrot", "image": "mars_game/img/carrot.png"}
        },
    }


    blocked_objects = bases + homes + greenhouses + map_objects

    resources = spawn_resources(resource_types, 30, blocked_objects)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                pygame.quit()
                exit()
            if scene in ("menu", "settings", "about"):

                if scene == "menu":
                    result = menu.handle_event(event)
                    if result == "PLAY":
                        fade_start("__play__")
                    elif result == "SETTINGS":
                        fade_start("settings")
                    elif result == "ABOUT":
                        fade_start("about")
                    elif result == "EXIT":
                        fade_start("__exit__")
                elif scene == "settings":
                   show_fps, sound_volume = menu.handle_settings_event(event, show_fps, sound_volume)
                elif scene == "about":
                    menu.handle_about_event(event)
                continue
            
            if event.type == pygame.KEYDOWN:
                if show_greenhouse_menu:

                    recipe_keys = list(crop_recipes.keys())

                    if event.key == pygame.K_ESCAPE:
                        show_greenhouse_menu = False

                    elif event.key == pygame.K_UP:
                        greenhouse_selected -= 1

                        if greenhouse_selected < 0:
                            greenhouse_selected = len(recipe_keys) - 1

                    elif event.key == pygame.K_DOWN:
                        greenhouse_selected += 1

                        if greenhouse_selected >= len(recipe_keys):
                            greenhouse_selected = 0

                    elif event.key == pygame.K_RETURN:

                        if growing_crop is None or growing_ready:
                            growing_ready = False
                            selected_key = recipe_keys[greenhouse_selected]
                            recipe = crop_recipes[selected_key]

                            total_details = (
                                count_item(inventory, "detail")
                                + count_item(storage_inventory, "detail")
                            )

                            if total_details >= recipe["cost"]:

                                remove_details(
                                    inventory,
                                    storage_inventory,
                                    recipe["cost"]
                                )

                                growing_crop = selected_key
                                growing_timer = recipe["time"]
                                growing_ready = False

                    continue
                if show_home_computer:
                    if event.key == pygame.K_ESCAPE:
                        show_home_computer = False

                    elif event.key == pygame.K_LEFT:
                        home_info_selected -= 1
                        if home_info_selected < 0:
                            home_info_selected = 3

                    elif event.key == pygame.K_RIGHT:
                        home_info_selected += 1
                        if home_info_selected > 3:
                            home_info_selected = 0

                    continue

                if show_computer:
                    current_options_count = 4

                    if computer_menu == "player":
                        current_options_count = 3
                    elif computer_menu == "rover":
                        current_options_count = 3
                    elif computer_menu == "base":
                        current_options_count = 3
                    elif computer_menu == "process":
                        current_options_count = len(inventory) + len(storage_inventory)

                        if current_options_count < 1:
                            current_options_count = 1

                        if current_options_count > 15:
                            current_options_count = 15


                    if event.key == pygame.K_ESCAPE:
                        if computer_menu == "main":
                            show_computer = False
                        else:
                            computer_menu = "main"
                            computer_selected = 0

                    elif event.key == pygame.K_UP:
                        computer_selected -= 1
                        if computer_selected < 0:
                            computer_selected = current_options_count - 1

                    elif event.key == pygame.K_DOWN:
                        computer_selected += 1
                        if computer_selected >= current_options_count:
                            computer_selected = 0
                    elif event.key == pygame.K_LEFT:
                        if computer_menu == "process":
                            computer_selected -= 1
                            if computer_selected < 0:
                                computer_selected = current_options_count - 1

                    elif event.key == pygame.K_RIGHT:
                        if computer_menu == "process":
                            computer_selected += 1
                            if computer_selected >= current_options_count:
                                computer_selected = 0


                    elif event.key == pygame.K_RETURN:
                        if computer_menu == "main":
                            if computer_selected == 0:
                                computer_menu = "player"
                            elif computer_selected == 1:
                                computer_menu = "rover"
                            elif computer_selected == 2:
                                computer_menu = "base"
                            elif computer_selected == 3:
                                computer_menu = "process"
                                computer_selected = 0
                        elif computer_menu == "process":
                            all_count = len(inventory) + len(storage_inventory)

                            if all_count > 0:

                                from_inventory = computer_selected < len(inventory)

                                if from_inventory:
                                    item = inventory.pop(computer_selected)
                                else:
                                    storage_index = computer_selected - len(inventory)
                                    item = storage_inventory.pop(storage_index)

                                allowed_resources = {
                                    "mars_stone": 1,
                                    "big_mars_stone": 3,
                                }

                                if item["name"] in allowed_resources:
                                    details_count = allowed_resources[item["name"]]

                                    for _ in range(details_count):
                                        inventory.append(detail_item.copy())

                                else:
                                    if from_inventory:
                                        inventory.insert(computer_selected, item)
                                    else:
                                        storage_inventory.insert(storage_index, item)

                            computer_selected = 0

                    continue

                if show_storage:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                        show_storage = False

                    elif event.key == pygame.K_LEFT:
                        if storage_side == "storage":
                            storage_side = "player"
                            selected_slot = 0
                        else:
                            selected_slot = max(0, selected_slot - 1)

                    elif event.key == pygame.K_RIGHT:
                        if storage_side == "player" and selected_slot % 3 == 2:
                            storage_side = "storage"
                            selected_slot = 0
                        else:
                            selected_slot = min(11, selected_slot + 1)

                    elif event.key == pygame.K_UP:
                        selected_slot = max(0, selected_slot - 3)

                    elif event.key == pygame.K_DOWN:
                        selected_slot = min(11, selected_slot + 3)

                    elif event.key == pygame.K_f:
                        if storage_side == "player":
                            if selected_slot < len(inventory):
                                if len(storage_inventory) < 12:
                                    storage_inventory.append(inventory.pop(selected_slot))

                                    if selected_slot >= len(inventory):
                                        selected_slot = max(0, len(inventory) - 1)
                                else:
                                    storage_full_timer = 120

                        else:
                            if selected_slot < len(storage_inventory):
                                inventory.append(storage_inventory.pop(selected_slot))
                                if selected_slot >= len(storage_inventory):
                                    selected_slot = max(0, len(storage_inventory) - 1)

                    continue

                if event.key == pygame.K_TAB:
                    show_inventory = not show_inventory

                if event.key == pygame.K_q and scene == "mars":
                    if in_rover:
                        in_rover = False
                        active_player = human
                        human.x = rover.x + 160
                        human.y = rover.y + 40
                        human.vel_x = 0
                        human.vel_y = 0
                        rover.vel_x = 0
                        rover.vel_y = 0

                if event.key == pygame.K_e and scene == "base":
                    if human.get_rect().colliderect(base_exit_rect.inflate(40, 40)):
                        scene = "mars"
                        active_player = human
                        in_rover = False

                        human.x = base.x + 150
                        human.y = base.y + 390
                        human.vel_x = 0
                        human.vel_y = 0

                    elif human.get_rect().colliderect(computer_rect.inflate(60, 60)):
                        show_computer = True
                        show_inventory = False
                        show_storage = False
                        computer_menu = "main"
                        computer_selected = 0
                    elif human.get_rect().colliderect(storage_rect.inflate(80, 80)):
                        show_storage = True
                        show_inventory = False
                        show_computer = False
                        storage_side = "player" 
                        selected_slot = 0


                    elif human.get_rect().colliderect(locked_storage_rect.inflate(60, 60)):
                        locked_message_timer = 120

                    elif human.get_rect().colliderect(locked_storage_rect2.inflate(60, 60)):
                        locked_message_timer = 120

                    elif not in_rover and rover_inside_base:   
                        if human.get_rect().colliderect(rover.get_rect().inflate(80, 80)):
                            in_rover = True
                            scene = "mars"
                            rover_inside_base = False
                            
                            active_player = rover

                            rover.x = base.x + 120
                            rover.y = base.y + 330
                            rover.vel_x = 0
                            rover.vel_y = 0

                elif event.key == pygame.K_e and scene == "mars":
                    if not in_rover:               
                        if not rover_inside_base and human.get_rect().colliderect(rover.get_rect().inflate(120, 120)):
                            in_rover = True
                            active_player = rover
                            human.x = rover.x   
                            human.y = rover.y
                            human.vel_x = 0
                            human.vel_y = 0
                        else:
                            for base in bases:
                                if base.can_interact(human):
                                    scene = "base"
                                    active_player = human
                                    in_rover = False

                                    human.x = 600
                                    human.y = 520
                                    human.vel_x = 0
                                    human.vel_y = 0
                                    break

                            if scene == "mars":
                                for h in homes:
                                    if h.can_interact(human):
                                        scene = "home"
                                        human.x = 500
                                        human.y = 500
                                        human.vel_x = 0
                                        human.vel_y = 0
                                        break

                            if scene == "mars":
                                for g in greenhouses:
                                    if g.can_interact(human):
                                        scene = "greenhouse"
                                        human.x = 500
                                        human.y = 500
                                        human.vel_x = 0
                                        human.vel_y = 0
                                        break


                    else:
                        for base in bases:
                            if base.can_interact(rover):
                                scene = "base"
                                in_rover = False
                                active_player = human
                                rover_inside_base = True

                                human.x = 600
                                human.y = 520
                                human.vel_x = 0
                                human.vel_y = 0

                                rover.x = 430
                                rover.y = 520
                                rover.vel_x = 0
                                rover.vel_y = 0     
                elif event.key == pygame.K_e and scene == "home":
                    if human.get_rect().colliderect(home_computer_rect.inflate(60, 60)):
                        show_home_computer = True
                        show_inventory = False
                        show_storage = False
                        show_computer = False
                        home_info_selected = 0

                    elif home.is_near_door(human):
                        scene = "mars"
                        human.x = home.x + 140
                        human.y = home.y + 200
                        human.vel_x = 0
                        human.vel_y = 0

                elif event.key == pygame.K_e and scene == "greenhouse":

                    if human.get_rect().colliderect(greenhouse_computer_rect.inflate(60, 60)):
                        show_greenhouse_menu = True
                        greenhouse_selected = 0

                    elif greenhouse.is_near_door(human):
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
        keys = pygame.key.get_pressed()
        
        


        if scene == "mars" and not in_rover:
            near_resource = None

            for resource in resources:
                if resource.can_pickup(human):
                    near_resource = resource
                    break

            if keys[pygame.K_e] and near_resource is not None:
                if pickup_resource != near_resource:
                    pickup_resource = near_resource
                    pickup_progress = 0

                pickup_progress += 1 / FPS

                if pickup_progress >= pickup_resource.pickup_time:
                    inventory.append(pickup_resource.get_item_data())
                    resources.remove(pickup_resource)
                    pickup_resource = None
                    pickup_progress = 0
            else:
                pickup_resource = None
                pickup_progress = 0
        else:
            pickup_resource = None
            pickup_progress = 0



        if active_player == human:
            human.animate()

        
        
        if scene == "mars":
            buildings = homes + greenhouses + map_objects
            if in_rover:              
                rover.update(WIDTH, HEIGHT, bases, buildings)
                target_camera_x = active_player.x - WIDTH // 2
                target_camera_y = active_player.y - HEIGHT // 2

                camera_x += (target_camera_x - camera_x) * 0.08
                camera_y += (target_camera_y - camera_y) * 0.08

            else:
                if rover_inside_base:
                    human.update_mars(bases, None, buildings)
                else:
                    human.update_mars(bases, rover, buildings)

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
            for obj in map_objects:
                obj.draw(screen, camera_x, camera_y)
            for resource in resources:
                resource.draw(screen, camera_x, camera_y)
            if pickup_resource is not None:
                draw_pickup_bar(screen, pickup_resource, pickup_progress, camera_x, camera_y)


            if not rover_inside_base:
                rover.draw(screen, camera_x, camera_y)

            if not in_rover:
                human.draw_mars(screen, camera_x, camera_y)


        elif scene == "base":
            if active_player == human:
                if rover_inside_base:
                    human.update_inside_base(base_walls, rover)
                else:
                    human.update_inside_base(base_walls)
            else:
                active_player.update_inside_base(base_walls)

            screen.blit(base_bg, (0, 0))

            if rover_inside_base:
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
   

        if show_inventory:
            draw_inventory(screen, inventory)

        if show_storage:
            draw_storage_window(screen, inventory, storage_inventory, storage_side, selected_slot)
        if locked_message_timer > 0:
            locked_message_timer -= 1
            font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)
            message = font.render("Storage is locked!", True, (255, 180, 80))

            msg_x = WIDTH // 2 - message.get_width() // 2
            msg_y = HEIGHT // 2 - message.get_height() // 2

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (msg_x - 20, msg_y - 12, message.get_width() + 40, message.get_height() + 24)
            )
            screen.blit(message, (msg_x, msg_y))
        if storage_full_timer > 0:
            storage_full_timer -= 1

            font = pygame.font.Font("mars_game/fonts/PressStart2P-Regular.ttf", 16)
            message = font.render("STORAGE FULL!", True, (255, 180, 80))

            msg_x = WIDTH // 2 - message.get_width() // 2
            msg_y = HEIGHT // 2 - message.get_height() // 2 + 60

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (msg_x - 20, msg_y - 12, message.get_width() + 40, message.get_height() + 24)
            )
            screen.blit(message, (msg_x, msg_y))

        if show_computer:
            draw_computer_menu(screen, computer_menu, computer_selected, inventory, storage_inventory)
        if show_home_computer:
            draw_home_computer(screen, home_info_selected, rover_inside_base, inventory, storage_inventory, resources)
        if show_greenhouse_menu:
            draw_greenhouse_menu(
                screen,
                greenhouse_selected,
                crop_recipes,
                growing_crop,
                growing_timer,
                growing_ready
            )
                    
        if growing_crop is not None and not growing_ready:
            growing_timer -= 1

            if growing_timer <= 0:
                growing_ready = True
                
                recipe = crop_recipes[growing_crop]

                inventory.append(recipe["item"].copy())
        new_scene = fade_update()
        if new_scene == "__play__":
            scene = "base"
            human.x = 600
            human.y = 520
            human.vel_x = 0
            human.vel_y = 0
            active_player = human
            in_rover = False
            rover_inside_base = True
        elif new_scene == "__exit__":
            pygame.quit()
            exit()
        elif new_scene is not None:
            scene = new_scene

        if scene in ("menu", "settings", "about"):
            if scene == "menu":
                menu.update()
                menu.draw(screen)
            elif scene == "settings":
                menu.update()
                menu.draw_settings(screen, show_fps, sound_volume)
            elif scene == "about":
                menu.update()
                menu.draw_about(screen)
            fade_draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        fade_draw(screen)

              
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

