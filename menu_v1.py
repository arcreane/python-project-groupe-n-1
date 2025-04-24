import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Game : La Salle du Tueur")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

pygame.font.init()
font = pygame.font.Font(None, 50)

menu_options = ["Nouvelle Partie", "Charger une Partie", "Options", "Quitter"]
selected = 0

def menu():
    SCREEN.fill(BLACK)
    title = font.render("Escape Game : La Salle du Tueur", True, RED)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 400))

    for i, option in enumerate(menu_options):
        color = WHITE if i == selected else GRAY
        text = font.render(option, True, color)
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, 500 + i * 60))

    pygame.display.flip()

running = True
while running:
    menu()
    
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
                    import scene1.py
                elif selected == 1:
                    print("Chargement des sauvegardes...")
                elif selected == 2:
                    print("Options...")
                elif selected == 3:
                    running = False

pygame.quit()
sys.exit()
