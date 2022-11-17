import pygame 
import random
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Test game')
screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN if 640 == 0 else 0)
display = pygame.Surface((640, 480))
player = {'x':0, 'y':0, 'r':25}
camera = {'x':-320, 'y':-240}

font = pygame.font.Font('PixeloidMono-1G8ae.ttf', 9)

running = True

enemies = []

MAIN_MENU = 0
RUN_GAME = 1
PAUSE_MENU = 2
GAME_OVER = 3
VICTORY = 4
ONLINE_GAME = 5

game_state = MAIN_MENU

menu_ptr = 0

def apply_camera(char, camera):
    return (char['x']-camera['x'], char['y']-camera['y'])

def distance(p1, p2):
    distX = p1['x'] - p2['x']
    distY = p1['y'] - p2['y']
    dist = ((distX**2) + (distY**2)) ** (1/2)
    if dist <= (p1['r'] + p2['r']):
        return True
    return False

def print_text(font, display, text, x, y, color=(255,255,255), bg_color=None, alpha=255, scale=1.0, center=True):
    str_list = []
    temp_i = -1
    for i in range(len(text)):
        if text[i] == "\n":
            str_list.append(text[temp_i+1:i])
            temp_i = i
    str_list.append(text[temp_i+1:])

    for i in range(len(str_list)):
        if bg_color is None:
            text_surface = font.render(str_list[i], True, color)
        else:
            text_surface = font.render(str_list[i], True, color, bg_color)
        text_surface.set_alpha(alpha)
        text_surface = pygame.transform.scale(text_surface, [text_surface.get_width()*scale, text_surface.get_height()*scale])
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y+(i*text_rect.height)
        if center:
            text_rect.midtop = (x, y+((i+1)*text_rect.height))
        display.blit(text_surface, text_rect)

while running:
    display.fill((64, 0, 128))

    if game_state == MAIN_MENU:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_UP]:
                    menu_ptr -= 1
                    if menu_ptr < 0:
                        menu_ptr = 2
                if keys[K_DOWN]:
                    menu_ptr +=1
                    if menu_ptr > 2:
                        menu_ptr = 0
                if keys[K_RETURN]:
                    if menu_ptr == 0:
                        game_state = RUN_GAME

                        player['x'] = 0
                        player['y'] = 0
                        player['r'] = 25

                        camera['x'] = -320
                        camera['y'] = -240

                        enemies_qt = random.randint(16, 30)

                        while enemies_qt > len(enemies):
                            enemy = {}
                            enemy['color'] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                            enemy['r'] = random.randint(5,75)
                            enemy['x'] = random.randint(-1500, 1500)
                            enemy['y'] = random.randint(-1500, 1500)

                            found_collision = False

                            for test in enemies:
                                colliding = distance(test, enemy)
                                
                                if colliding:
                                    found_collision = True

                            if not found_collision and not distance(player, enemy):
                                enemies.append(enemy)


                    if menu_ptr == 2:
                        running = False 

        print_text(font, display, "Start", 320, 100, scale=4, alpha=(255 if menu_ptr == 0 else 64))
        print_text(font, display, "Online", 320, 150, scale=4, alpha=(255 if menu_ptr == 1 else 64))
        print_text(font, display, "Quit", 320, 200, scale=4, alpha=(255 if menu_ptr == 2 else 64))
    
    elif game_state == RUN_GAME:

        print_text(font, display, f"Enemies: {len(enemies)}", 10, 10, center=False)
        print_text(font, display, f"Coords: {player['x']}, {player['y']}", 450, 10, center=False)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and player['x'] <= 1500:
            player['x'] += 1
            camera['x'] += 1
        if keys[K_LEFT] and player['x'] >= -1500:
            player['x'] -= 1
            camera['x'] -= 1
        if keys [K_UP] and player['y'] >= -1500:
            player['y'] -= 1
            camera['y'] -= 1
        if keys [K_DOWN] and player['y'] <= 1500:
            player['y'] += 1
            camera['y'] += 1

        for i in range(-1500, 1501, 50):
            start_coords = apply_camera({'x':i, 'y':-1500}, camera)
            if start_coords[0] > 0 and start_coords[0] < 640:
                pygame.draw.line(display, (100, 64, 255), start_coords, apply_camera({'x':i, 'y':1500}, camera))

            start_coords = apply_camera({'x':-1500, 'y':i}, camera)
            if start_coords[1] > 0 and start_coords[1] < 448:    
                pygame.draw.line(display, (100, 64, 255), start_coords, apply_camera({'x':1500, 'y':i}, camera))

        for enemy in enemies:
            enemy_coords = apply_camera(enemy, camera)
            if enemy_coords[0]+enemy['r'] > 0 and enemy_coords[0]-enemy['r'] < 640 and enemy_coords[1]+enemy['r'] > 0 and enemy_coords[1]-enemy['r'] < 448: 
                pygame.draw.circle(display, enemy['color'], enemy_coords, enemy['r'], 0)
                
                if distance(player, enemy):
                    print_text(font, display, "Collision detected", 10, 10, center=False)
                    if player['r'] > enemy['r']:
                        enemies.remove(enemy)
                        player['r'] += enemy['r']/2
                        if len(enemies) == 0:
                            game_state = VICTORY 
                            enemies = []
                    elif enemy['r'] > player['r'] :
                        game_state = GAME_OVER
                        enemies = []

        pygame.draw.circle(display, (110, 42, 235), apply_camera(player, camera), player['r'], 0)
        pygame.draw.circle(display, (255, 255, 255), apply_camera(player, camera), player['r'], 3)

    elif game_state == ONLINE_GAME:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False


    elif game_state == GAME_OVER:
        print_text(font, display, "GAME OVER", 320, 150, center=True, scale=4)
        print_text(font, display, "Press ENTER to return for main menu", 320, 250, center=True, scale=2)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[K_RETURN]:
                    game_state = MAIN_MENU

    elif game_state == VICTORY:
        print_text(font, display, "VICTORY!", 320, 150, center=True, scale=4)
        print_text(font, display, "Press ENTER to return for main menu", 320, 250, center=True, scale=2)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[K_RETURN]:
                    game_state = MAIN_MENU

    screen.blit(display, (0, 0))
    pygame.display.update()