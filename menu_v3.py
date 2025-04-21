import pygame
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Game : La Salle du Tueur")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (150, 150, 150)
LIGHT_RED = (255, 50, 50)

background = pygame.image.load("gradient.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
rectangle = pygame.image.load("rectangle.png")
rectangle = pygame.transform.scale(rectangle, (700, 650))
rectangle.set_alpha(80)

# Police
title_font = pygame.font.Font(None, 100)
menu_font = pygame.font.Font(None, 60)

# Options du menu
menu_options = ["Nouvelle Partie", "Charger une Partie", "Options", "Quitter"]
selected = 0

# Affichage du menu
def draw_menu():
    SCREEN.blit(background, (0, 0))
    SCREEN.blit(rectangle, (610,230))

    # Titre
    title = title_font.render("Escape Game", True, RED)
    subtitle = menu_font.render("La Salle du Tueur", True, WHITE)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 350))
    SCREEN.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 430))

    # Options
    for i, option in enumerate(menu_options):
        color = LIGHT_RED if i == selected else GRAY
        text = menu_font.render(option, True, color)
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, 550 + i * 60))

    pygame.display.flip()

# Boucle principale
running = True
while running:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(menu_options)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected == 0:
                    print("Nouvelle Partie...")
                    import Salle1_v0.py
                elif selected == 1:
                    print("Chargement des sauvegardes...")
                elif selected == 2:
                    print("Options...")
                elif selected == 3:
                    running = False

pygame.quit()
sys.exit()
