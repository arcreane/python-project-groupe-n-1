import pygame
import sys

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Death Run - La Mort poursuit le joueur")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)

# Joueur
player_width, player_height = 30, 60
player_pos = [WIDTH // 4, HEIGHT - player_height - 100]
player_speed = 5
player_velocity = 0  # Pour gérer la gravité

# La Mort (bonhomme rouge)
death_width, death_height = 30, 60
death_pos = [player_pos[0] - 100, player_pos[1]]  # Position initiale derrière le joueur
death_speed = 2  # Vitesse de La Mort

# Terrain
terrain_points = [[i, HEIGHT - 100 + (i % 300) - (i % 600)] for i in range(0, WIDTH * 2, 100)]

# Gravité
gravity = 1

# Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Quitter le jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement horizontal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
        for point in terrain_points:
            point[0] -= player_speed  # Décor avance avec le joueur
        death_pos[0] += player_speed  # La Mort suit le joueur
    if keys[pygame.K_LEFT] and player_pos[0] > WIDTH // 4:
        player_pos[0] -= player_speed
        for point in terrain_points:
            point[0] += player_speed  # Décor recule avec le joueur
        death_pos[0] -= player_speed  # La Mort suit le joueur

    # Gravité et ajustement vertical
    player_velocity += gravity
    player_pos[1] += player_velocity
    death_pos[1] += gravity  # La Mort est aussi affectée par la gravité
    for i in range(len(terrain_points) - 1):
        if terrain_points[i][0] <= player_pos[0] <= terrain_points[i + 1][0]:
            # Trouver la hauteur du terrain
            terrain_slope = (terrain_points[i + 1][1] - terrain_points[i][1]) / (terrain_points[i + 1][0] - terrain_points[i][0])
            terrain_y = terrain_points[i][1] + terrain_slope * (player_pos[0] - terrain_points[i][0])
            if player_pos[1] > terrain_y:
                player_pos[1] = terrain_y
                player_velocity = 0  # Arrêter la gravité lorsqu'on touche le sol
            # Ajuster La Mort à la hauteur du terrain
            terrain_y_death = terrain_points[i][1] + terrain_slope * (death_pos[0] - terrain_points[i][0])
            if death_pos[1] > terrain_y_death:
                death_pos[1] = terrain_y_death

    # Déplacement de La Mort vers le joueur
    if player_pos[0] > death_pos[0]:
        death_pos[0] += death_speed  # La Mort avance vers le joueur
    if player_pos[0] < death_pos[0]:
        death_pos[0] -= death_speed  # La Mort recule si le joueur recule

    # Dessiner le terrain
    for i in range(len(terrain_points) - 1):
        pygame.draw.line(screen, GREEN, terrain_points[i], terrain_points[i + 1], 5)

    # Dessiner le joueur
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_width, player_height))

    # Dessiner La Mort
    pygame.draw.rect(screen, RED, (death_pos[0], death_pos[1], death_width, death_height))

    # Vérifier si La Mort rattrape le joueur
    if (
        death_pos[0] < player_pos[0] + player_width and
        death_pos[0] + death_width > player_pos[0] and
        death_pos[1] < player_pos[1] + player_height and
        death_pos[1] + death_height > player_pos[1]
    ):
        text = font.render("La Mort vous a rattrapé !", True, RED)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # Mettre à jour l'écran
    pygame.display.update()

    # Contrôler la vitesse
    clock.tick(30)

pygame.quit()
sys.exit()