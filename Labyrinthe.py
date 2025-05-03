import pygame
import random
import time
import math
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1200, 900
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Menu du Jeu')

# Chargement des images
background_image = pygame.image.load('backgroundSalle.png')
background_image = pygame.transform.scale(background_image, (LARGEUR, HAUTEUR))
player_image = pygame.image.load('Walk1.png')
player_image = pygame.transform.scale(player_image, (150, 150))  # Augmentation de la taille du personnage

# Positions initiales
player_x, player_y = 50, HAUTEUR - 200
player_speed = 2
arcade_x, arcade_y = 900, HAUTEUR - 200
door_x, door_y = 200, HAUTEUR - 200

# Fonctions de dessin
def dessiner_joueur(x, y):
    screen.blit(player_image, (x, y))

def dessiner_borne_arcade(x, y):
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 150))


def dessiner_porte(x, y):
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 150))

# Fonction pour lancer le jeu
def lancer_jeu():
    global x_player, y_player  # Utilisation de variables globales

    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption('Jeu de Labyrinthe avec Compte à Rebours')

    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    BLEU = (0, 0, 255)

    ImgChemin = pygame.image.load('pierres-empilees_1194-5596.png')
    ImgForet = pygame.image.load('istockphoto-1388629426-640x640.jpg')
    ImgJoueur = pygame.image.load('Walk1.png')

    NB_CELLULES_X, NB_CELLULES_Y = 40, 30
    TAILLE_CELLULE = 30

    ImgChemin = pygame.transform.scale(ImgChemin, (TAILLE_CELLULE, TAILLE_CELLULE))
    ImgForet = pygame.transform.scale(ImgForet, (TAILLE_CELLULE, TAILLE_CELLULE))
    ImgJoueur = pygame.transform.scale(ImgJoueur, (TAILLE_CELLULE + 10, TAILLE_CELLULE + 10))

    def generer_labyrinthe():
        labyrinthe = [[1 for _ in range(NB_CELLULES_X)] for _ in range(NB_CELLULES_Y)]
        visite = [[False for _ in range(NB_CELLULES_X)] for _ in range(NB_CELLULES_Y)]

        def dessiner_chemin(x, y):
            labyrinthe[y][x] = 0
            visite[y][x] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def backtrack(x, y):
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 < nx < NB_CELLULES_X and 0 < ny < NB_CELLULES_Y and not visite[ny][nx]:
                    labyrinthe[ny][nx] = 0
                    labyrinthe[y + dy][x + dx] = 0
                    visite[ny][nx] = True
                    backtrack(nx, ny)

        dessiner_chemin(1, 1)
        backtrack(1, 1)

        return labyrinthe

    labyrinthe = generer_labyrinthe()
    x_player, y_player = 1, 1

    def generer_sortie():
        while True:
            x, y = random.randint(1, NB_CELLULES_X - 2), random.randint(1, NB_CELLULES_Y - 2)
            distance = math.hypot(x - 1, y - 1)
            if labyrinthe[y][x] == 0 and distance > 5:
                return x, y

    x_sortie, y_sortie = generer_sortie()

    FPS = 10
    clock = pygame.time.Clock()

    TEMPS_TOTAL = 60
    debut = time.time()

    def dessiner_labyrinthe():
        for y in range(NB_CELLULES_Y):
            for x in range(NB_CELLULES_X):
                rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
                screen.blit(ImgForet if labyrinthe[y][x] == 1 else ImgChemin, rect)

    def dessiner_joueur(x, y):
        rect = pygame.Rect(x * TAILLE_CELLULE - 5, y * TAILLE_CELLULE - 10, TAILLE_CELLULE + 10, TAILLE_CELLULE + 10)
        screen.blit(ImgJoueur, rect)

    def dessiner_sortie(x, y):
        pygame.draw.rect(screen, BLEU, (x * TAILLE_CELLULE + 10, y * TAILLE_CELLULE + 10, TAILLE_CELLULE - 20, TAILLE_CELLULE - 20))
        pygame.draw.line(screen, (255, 0, 0), (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 10),
                         (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 40), 3)
        pygame.draw.polygon(screen, (255, 0, 0),
                            [(x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 10),
                             (x * TAILLE_CELLULE + 45, y * TAILLE_CELLULE + 20),
                             (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 30)])

    def deplacer_joueur(dx, dy):
        global x_player, y_player  # Utilisation de variables globales
        if 0 <= x_player + dx < NB_CELLULES_X and 0 <= y_player + dy < NB_CELLULES_Y:
            if labyrinthe[y_player + dy][x_player + dx] == 0:
                x_player += dx
                y_player += dy

    def sortie_atteinte():
        return x_player == x_sortie and y_player == y_sortie

    running = True
    temps_restant = TEMPS_TOTAL

    while running:
        temps_restant = TEMPS_TOTAL - int(time.time() - debut)
        if temps_restant <= 0:
            temps_restant = 0
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            deplacer_joueur(-1, 0)
        elif touches[pygame.K_RIGHT]:
            deplacer_joueur(1, 0)
        elif touches[pygame.K_UP]:
            deplacer_joueur(0, -1)
        elif touches[pygame.K_DOWN]:
            deplacer_joueur(0, 1)

        screen.fill(BLANC)
        dessiner_labyrinthe()
        dessiner_joueur(x_player, y_player)
        dessiner_sortie(x_sortie, y_sortie)

        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Temps restant : {temps_restant}s", True, NOIR)
        screen.blit(timer_text, (10, 10))

        if sortie_atteinte():
            texte = font.render("Vous avez trouvé la sortie !", True, (0, 255, 0))
            screen.blit(texte, (LARGEUR // 2 - 150, HAUTEUR // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            return True

        pygame.display.flip()
        clock.tick(FPS)

    while True:
        screen.fill(BLANC)
        font = pygame.font.Font(None, 48)
        texte = font.render("Temps écoulé ! Vous avez perdu.", True, (255, 0, 0))
        screen.blit(texte, (LARGEUR // 2 - 250, HAUTEUR // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(3000)
        return False

# Boucle principale
running = True
result = False  # Initialisation de la variable result
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement du personnage
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Vérification de la collision avec la borne d'arcade

    player_rect = pygame.Rect(player_x, player_y, 150, 150)
    arcade_rect = pygame.Rect(arcade_x, arcade_y, 100, 150)
    door_rect = pygame.Rect(door_x, door_y, 100, 150)

    if player_rect.colliderect(arcade_rect):
        result = lancer_jeu()
        if result:
            player_x, player_y = 100, HAUTEUR - 100
        else:
            player_x, player_y = 100, HAUTEUR - 100

    if result and player_rect.colliderect(door_rect):
        pygame.quit()
        sys.exit()

    # Dessiner les éléments
    screen.blit(background_image, (0, 0))
    dessiner_joueur(player_x, player_y)
    dessiner_borne_arcade(arcade_x, arcade_y)
    if result:
        dessiner_porte(door_x, door_y)

    pygame.display.flip()

pygame.quit()
