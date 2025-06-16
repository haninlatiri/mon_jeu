import pygame
import random
from pygame.locals import *

# Initialisation
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ballon Volant")

# Charger la musique (elle sera lancée au démarrage du jeu, pas dans le menu)
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)

# Couleurs
blue = (113, 177, 227)
white = (255, 255, 255)
dark_blue = (50, 90, 150)
grey = (200, 200, 200)
black =(0,0,0)

# Police
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

# Charger les images
try:
    ballon_img = pygame.image.load('ballon.png').convert_alpha()
    ballon_img = pygame.transform.scale(ballon_img, (90, 90))
except:
    ballon_img = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.circle(ballon_img, (255, 0, 0), (30, 30), 30)

try:
    fond_menu = pygame.image.load('fond.png').convert()
    fond_menu = pygame.transform.scale(fond_menu, (screen_width, screen_height))
except:
    fond_menu = pygame.Surface((screen_width, screen_height))
    fond_menu.fill(dark_blue)

cloud_img = pygame.Surface((200, 150), pygame.SRCALPHA)
pygame.draw.ellipse(cloud_img, (240, 240, 240), (0, 0, 200, 150))

clock = pygame.time.Clock()

def game_over(score):
    text = font.render(f"Game Over - Score: {score}", True, black)
    screen.blit(text, (screen_width//2 - 100, screen_height//2))
    pygame.display.flip()
    pygame.time.wait(2000)

def game_loop():
    pygame.mixer.music.play(-1)  # Lancer la musique en boucle

    ballon_rect = ballon_img.get_rect(center=(100, screen_height // 2))
    ballon_speed = 3
    ballon_alive = True

    cloud_groups = [
        {'x': 600, 'y': 100, 'passed': False},
        {'x': 1000, 'y': 300, 'passed': False}
    ]
    cloud_speed = 2
    vertical_gap = 200
    horizontal_gap = 400
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_UP and ballon_alive:
                    ballon_rect.y -= 50
                if event.key == K_DOWN and ballon_alive:
                    ballon_rect.y += 50

        if ballon_alive:
            ballon_rect.x += ballon_speed
        # Empêcher le ballon de sortir de l'écran à droite
        if ballon_rect.right > screen_width:
            ballon_rect.right = screen_width
        # Et à gauche si jamais tu permets un retour en arrière
        if ballon_rect.left < 0:
            ballon_rect.left = 0

        for group in cloud_groups:
            group['x'] -= cloud_speed

            if group['x'] < -200:
                group['x'] = max(g['x'] for g in cloud_groups) + horizontal_gap
                group['y'] = random.randint(50, screen_height - vertical_gap - 150)
                group['passed'] = False

        if ballon_alive:
            for group in cloud_groups:
                top_cloud = pygame.Rect(group['x'], group['y'] - vertical_gap, 200, 150)
                bottom_cloud = pygame.Rect(group['x'], group['y'] + vertical_gap, 200, 150)

                if ballon_rect.colliderect(top_cloud) or ballon_rect.colliderect(bottom_cloud):
                    ballon_alive = False

                if ballon_rect.x > group['x'] + 200 and not group['passed']:
                    group['passed'] = True
                    score += 1

        screen.fill(blue)

        for group in cloud_groups:
            screen.blit(cloud_img, (group['x'], group['y'] - vertical_gap))
            screen.blit(cloud_img, (group['x'], group['y'] + vertical_gap))

        if ballon_alive:
            screen.blit(ballon_img, ballon_rect)
        else:
            game_over(score)
            return

        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

def menu():
    button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    in_menu = True

    while in_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    in_menu = False

        screen.blit(fond_menu, (0, 0))

        title = big_font.render("Ballon Volant", True, white)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 150))

        pygame.draw.rect(screen, grey, button_rect, border_radius=10)
        text = font.render("START", True, dark_blue)
        screen.blit(text, (button_rect.x + 25, button_rect.y + 10))

        pygame.display.flip()
        clock.tick(60)

# Lancer le menu, puis le jeu
menu()
game_loop()






