import pygame
import random
import time

pygame.init()

LARGEUR, HAUTEUR = 1200, 900
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Jeu de Labyrinthe avec Compte à Rebours')

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

ImgChemin = pygame.image.load('pierres-empilees_1194-5596.png')
ImgForet = pygame.image.load('istockphoto-1388629426-640x640.jpg')

NB_CELLULES_X = 40
NB_CELLULES_Y = 30
TAILLE_CELLULE = 30
ImgChemin = pygame.transform.scale(ImgChemin, (TAILLE_CELLULE, TAILLE_CELLULE))
ImgForet = pygame.transform.scale(ImgForet, (TAILLE_CELLULE, TAILLE_CELLULE))

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
        x_sortie = random.randint(1, NB_CELLULES_X - 2)
        y_sortie = random.randint(1, NB_CELLULES_Y - 2)
        if labyrinthe[y_sortie][x_sortie] == 0:
            return x_sortie, y_sortie

x_sortie, y_sortie = generer_sortie()

FPS = 10
clock = pygame.time.Clock()

# Temps en secondes
TEMPS_TOTAL = 60
debut = time.time()

def dessiner_labyrinthe():
    for y in range(NB_CELLULES_Y):
        for x in range(NB_CELLULES_X):
            rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE)
            if labyrinthe[y][x] == 1:
                screen.blit(ImgForet, rect)
            else:
                screen.blit(ImgChemin, rect)

def dessiner_joueur(x, y):
    pygame.draw.rect(screen, ROUGE, (x * TAILLE_CELLULE + 10, y * TAILLE_CELLULE + 10, TAILLE_CELLULE - 20, TAILLE_CELLULE - 20))

def dessiner_sortie(x, y):
    pygame.draw.rect(screen, BLEU, (x * TAILLE_CELLULE + 10, y * TAILLE_CELLULE + 10, TAILLE_CELLULE - 20, TAILLE_CELLULE - 20))
    pygame.draw.line(screen, (255, 0, 0), (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 10),
                     (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 40), 3)
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 10),
                         (x * TAILLE_CELLULE + 45, y * TAILLE_CELLULE + 20),
                         (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 30)])

def deplacer_joueur(dx, dy):
    global x_player, y_player
    if 0 <= x_player + dx < NB_CELLULES_X and 0 <= y_player + dy < NB_CELLULES_Y:
        if labyrinthe[y_player + dy][x_player + dx] == 0:
            x_player += dx
            y_player += dy

def sortie_atteinte():
    return x_player == x_sortie and y_player == y_sortie

running = True
while running:
    temps_restant = TEMPS_TOTAL - int(time.time() - debut)
    if temps_restant <= 0:
        temps_restant = 0
        running = False  # Temps écoulé, on arrête le jeu

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
    timer_text = font.render(f"Temps restant : {temps_restant}s", True, ROUGE)
    screen.blit(timer_text, (10, 10))

    if sortie_atteinte():
        texte = font.render("Vous avez trouvé la sortie !", True, (0, 255, 0))
        screen.blit(texte, (LARGEUR // 2 - 150, HAUTEUR // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

# Afficher fin du temps si pas gagné
if temps_restant == 0 and not sortie_atteinte():
    screen.fill(BLANC)
    font = pygame.font.Font(None, 48)
    texte = font.render("Temps écoulé ! Vous avez perdu.", True, (255, 0, 0))
    screen.blit(texte, (LARGEUR // 2 - 250, HAUTEUR // 2))
    pygame.display.flip()


    attente_fin = True
    while attente_fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                attente_fin = False

pygame.quit()
