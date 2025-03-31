import pygame
import random

# Initialiser pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1200, 900  # Plus grand pour un labyrinthe plus large
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Jeu de Labyrinthe avec Objectif')

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)  # Bonus
BLEU = (0, 0, 255)  # Drapeau de sortie

# Taille du labyrinthe (en cellules)
NB_CELLULES_X = 40  # Augmenter le nombre de cellules en X
NB_CELLULES_Y = 30  # Augmenter le nombre de cellules en Y
TAILLE_CELLULE = 30  # Taille d'une cellule en pixels (plus petit pour un plus grand labyrinthe)

# Fonction pour générer le labyrinthe par backtracking
def generer_labyrinthe():
    # Créer une matrice de murs
    labyrinthe = [[1 for _ in range(NB_CELLULES_X)] for _ in range(NB_CELLULES_Y)]

    # Créer un tableau de visites pour savoir quelles cellules ont été visitées
    visite = [[False for _ in range(NB_CELLULES_X)] for _ in range(NB_CELLULES_Y)]

    # Choisir un point de départ (en haut à gauche)
    def dessiner_chemin(x, y):
        labyrinthe[y][x] = 0
        visite[y][x] = True

    # Directions possibles (haut, bas, gauche, droite)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def backtrack(x, y):
        random.shuffle(directions)  # Mélanger les directions pour un labyrinthe aléatoire
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < NB_CELLULES_X and 0 < ny < NB_CELLULES_Y and not visite[ny][nx]:
                # Créer un chemin en supprimant les murs
                labyrinthe[ny][nx] = 0
                labyrinthe[y + dy][x + dx] = 0
                visite[ny][nx] = True
                backtrack(nx, ny)  # Appel récursif pour continuer le backtracking

    # Démarrer le processus de génération depuis (1, 1)
    dessiner_chemin(1, 1)
    backtrack(1, 1)

    return labyrinthe

# Générer un labyrinthe avec chemins continus
labyrinthe = generer_labyrinthe()

# Position de départ (le joueur commence sur un chemin valide)
x_player, y_player = 1, 1

# Générer l'objectif (bonus)
def generer_objectif():
    while True:
        x_obj = random.randint(1, NB_CELLULES_X - 2)
        y_obj = random.randint(1, NB_CELLULES_Y - 2)
        if labyrinthe[y_obj][x_obj] == 0:  # Vérifier que l'objectif est sur un chemin
            return x_obj, y_obj

# Définir la position de la sortie (un endroit unique)
def generer_sortie():
    while True:
        x_sortie = random.randint(1, NB_CELLULES_X - 2)
        y_sortie = random.randint(1, NB_CELLULES_Y - 2)
        if labyrinthe[y_sortie][x_sortie] == 0:  # Vérifier que la sortie est sur un chemin
            return x_sortie, y_sortie

x_objectif, y_objectif = generer_objectif()
x_sortie, y_sortie = generer_sortie()

# Vitesse du jeu (en FPS)
FPS = 10
clock = pygame.time.Clock()

# Variables du score bonus
score_bonus = 0

# Fonction pour dessiner le labyrinthe
def dessiner_labyrinthe():
    for y in range(NB_CELLULES_Y):
        for x in range(NB_CELLULES_X):
            couleur = NOIR if labyrinthe[y][x] == 1 else BLANC
            pygame.draw.rect(screen, couleur, (x * TAILLE_CELLULE, y * TAILLE_CELLULE, TAILLE_CELLULE, TAILLE_CELLULE))

# Fonction pour dessiner le joueur
def dessiner_joueur(x, y):
    pygame.draw.rect(screen, ROUGE, (x * TAILLE_CELLULE + 10, y * TAILLE_CELLULE + 10, TAILLE_CELLULE - 20, TAILLE_CELLULE - 20))

# Fonction pour dessiner l'objectif (bonus)
def dessiner_objectif(x, y):
    pygame.draw.rect(screen, JAUNE, (x * TAILLE_CELLULE + 10, y * TAILLE_CELLULE + 10, TAILLE_CELLULE - 20, TAILLE_CELLULE - 20))

# Fonction pour dessiner la sortie (drapeau)
def dessiner_sortie(x, y):
    pygame.draw.rect(screen, BLEU, (x * TAILLE_CELLULE + 10, y * TAILLE_CELLULE + 10, TAILLE_CELLULE - 20, TAILLE_CELLULE - 20))
    # Dessiner un simple rectangle pour simuler un drapeau à la sortie
    pygame.draw.line(screen, (255, 0, 0), (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 10),
                     (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 40), 3)
    pygame.draw.polygon(screen, (255, 0, 0),
                        [(x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 10),
                         (x * TAILLE_CELLULE + 45, y * TAILLE_CELLULE + 20),
                         (x * TAILLE_CELLULE + 15, y * TAILLE_CELLULE + 30)])

# Fonction pour déplacer le joueur
def deplacer_joueur(dx, dy):
    global x_player, y_player
    # Empêcher de sortir des limites du labyrinthe
    if 0 <= x_player + dx < NB_CELLULES_X and 0 <= y_player + dy < NB_CELLULES_Y:
        if labyrinthe[y_player + dy][x_player + dx] == 0:
            x_player += dx
            y_player += dy

# Vérifier si le joueur a atteint la sortie
def sortie_atteinte():
    return x_player == x_sortie and y_player == y_sortie

# Vérifier si le joueur a atteint l'objectif (bonus)
def objectif_atteint():
    global score_bonus
    if x_player == x_objectif and y_player == y_objectif:
        score_bonus += 1
        return True
    return False

# Vérifier si le joueur a récupéré le bonus (objectif)
def bonus_atteint():
    global score_bonus
    if x_player == x_objectif and y_player == y_objectif:
        score_bonus += 1

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                deplacer_joueur(-1, 0)
            elif event.key == pygame.K_RIGHT:
                deplacer_joueur(1, 0)
            elif event.key == pygame.K_UP:
                deplacer_joueur(0, -1)
            elif event.key == pygame.K_DOWN:
                deplacer_joueur(0, 1)

    # Remplir l'écran de blanc
    screen.fill(BLANC)

    # Dessiner le labyrinthe, le joueur, l'objectif (bonus) et la sortie
    dessiner_labyrinthe()
    dessiner_joueur(x_player, y_player)
    dessiner_objectif(x_objectif, y_objectif)
    dessiner_sortie(x_sortie, y_sortie)

    # Vérifier si le joueur a atteint la sortie
    if sortie_atteinte():
        font = pygame.font.Font(None, 36)
        texte = font.render("Vous avez trouvé la sortie!", True, (0, 255, 0))
        screen.blit(texte, (LARGEUR // 2 - 150, HAUTEUR // 2))
        running = False  # Arrêter le jeu quand le joueur atteint la sortie

    # Afficher le score de points bonus
    font = pygame.font.Font(None, 36)
    texte_score = font.render(f"Points Bonus: {score_bonus}", True, (0, 0, 0))
    screen.blit(texte_score, (10, 10))

    # Rafraîchir l'écran
    pygame.display.flip()

    # Limiter les FPS
    clock.tick(FPS)

pygame.quit()


