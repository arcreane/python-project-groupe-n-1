import pygame
import sys
import random
import time

# Initialisation de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Death run")
CLOCK = pygame.time.Clock()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Chargement des images
background_img = pygame.image.load('background_salle4.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

console_img = pygame.image.load('console.png')
console_img = pygame.transform.scale(console_img, (210, 210))

room_player_img = pygame.image.load('sprite.png')
room_player_img = pygame.transform.scale(room_player_img, (200, 200))

game_player_img = pygame.image.load('boy.png')
game_player_img = pygame.transform.scale(game_player_img, (60, 60))

obstacle_img = pygame.image.load('couteau.png')
obstacle_img = pygame.transform.scale(obstacle_img, (60, 60))

coin_img = pygame.image.load('coinnn.png')
coin_img = pygame.transform.scale(coin_img, (40, 30))

# Polices d'écriture
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# Fonction d'affichage d'un texte centré
def draw_text(text, color, y):
    t = font.render(text, True, color)
    SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, y))

# Fonction pour afficher les statistiques du joueur après la partie
def draw_stats(stats):
    y_offset = 360
    labels = {
        "obstacles_avoided": "Nombre d'obstacles évités :",
        "game_status": "Statut final :",
        "time_taken": "Temps écoulé :"
    }
    for key in ["obstacles_avoided", "game_status", "time_taken"]:
        label = labels[key]
        value = stats[key]
        if key == "time_taken":
            value = f"{value:.1f}"
        stat_text = small_font.render(f"{label} {value}", True, WHITE)
        SCREEN.blit(stat_text, (WIDTH // 2 - stat_text.get_width() // 2, y_offset))
        y_offset += 30

# Initialisation des variables du joueur
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 50)
player_speed = 10

# Fonction principale du mini-jeu Temple Run
def temple_run():
    global obstacle_timer, obstacles, coin_timer, coins, score
    global obstacle_speed, coin_speed, obstacle_interval, coin_interval
    global player_stats, player

    # Réinitialisation des variables
    obstacles = []
    coins = []
    obstacle_timer = 0
    coin_timer = 0
    score = 0
    obstacle_speed = 7
    coin_speed = 5
    obstacle_interval = 30
    coin_interval = 50
    player_stats = {"obstacles_avoided": 0, "game_status": "alive", "time_taken": 0.0}
    player.x, player.y = WIDTH // 2 - 25, HEIGHT - 100

    start_time = time.time()
    max_time = 50  # Temps maximum avant "mort naturelle"
    running = True

    while running:
        SCREEN.fill(BLACK)
        elapsed_time = time.time() - start_time

        # Si le temps est écoulé, le joueur perd
        if elapsed_time >= max_time:
            player_stats["game_status"] = "en enfer"
            player_stats["time_taken"] = elapsed_time
            draw_text("La mort vous a attrapé !", RED, HEIGHT // 2)
            draw_stats(player_stats)
            pygame.display.flip()
            pygame.time.wait(4000)
            pygame.quit()
            sys.exit()

        # Contrôles du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
            player.x += player_speed

        # Génération des obstacles
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacle_timer = 0
            x_pos = random.randint(0, WIDTH - 50)
            obstacles.append(pygame.Rect(x_pos, -50, 50, 50))

        # Génération des pièces
        coin_timer += 1
        if coin_timer >= coin_interval:
            coin_timer = 0
            x_pos = random.randint(0, WIDTH - 30)
            coins.append(pygame.Rect(x_pos, -30, 30, 30))

        # Déplacement et gestion des collisions avec les obstacles
        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.y > HEIGHT:
                obstacles.remove(obs)
                player_stats["obstacles_avoided"] += 1
            if player.colliderect(obs):
                player_stats["game_status"] = "mort"
                player_stats["time_taken"] = elapsed_time
                draw_text("Game Over!", RED, HEIGHT // 2)
                draw_stats(player_stats)
                pygame.display.flip()
                pygame.time.wait(4000)
                pygame.quit()
                sys.exit()

        # Déplacement et collisions avec les pièces
        for coin in coins[:]:
            coin.y += coin_speed
            if coin.y > HEIGHT:
                coins.remove(coin)
            if player.colliderect(coin):
                score += 1
                coins.remove(coin)

        # Augmentation progressive de la difficulté
        if score > 0 and score % 5 == 0:
            obstacle_speed = 7 + score // 5
            coin_speed = 5 + score // 6
            obstacle_interval = max(15, 30 - score)

        # Si le joueur atteint 20 pièces, il gagne
        if score >= 20:
            player_stats["game_status"] = "échappé"
            player_stats["time_taken"] = elapsed_time
            draw_text("Victoire! Vous vous êtes échappé!", GREEN, HEIGHT // 2)
            draw_stats(player_stats)
            pygame.display.flip()
            pygame.time.wait(4000)
            return True

        # Affichage des éléments du jeu
        SCREEN.blit(game_player_img, player.topleft)
        for obs in obstacles:
            SCREEN.blit(obstacle_img, obs.topleft)
        for coin in coins:
            SCREEN.blit(coin_img, coin.topleft)

        draw_text(f"Score: {score}/20", WHITE, 60)

        pygame.display.flip()
        CLOCK.tick(30)

        # Événements système (fermeture de la fenêtre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return True

# Salle principale du jeu où l'on lance le mini-jeu
def main_room():
    room_player = pygame.Rect(150, HEIGHT - 200, 70, 70)
    console = pygame.Rect(WIDTH - 240, HEIGHT - 200, 70, 70)
    running = True

    while running:
        SCREEN.blit(background_img, (0, 0))

        # Mouvements dans la salle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and room_player.x > 0:
            room_player.x -= player_speed
        if keys[pygame.K_RIGHT] and room_player.x < WIDTH - room_player.width:
            room_player.x += player_speed

        # Affichage des éléments de la salle
        SCREEN.blit(console_img, console.topleft)
        SCREEN.blit(room_player_img, room_player.topleft)

        # Interaction avec la console
        if room_player.colliderect(console):
            hint = small_font.render("Appuyez sur A pour lancer le jeu", True, WHITE)
            SCREEN.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2))
            if keys[pygame.K_a]:
                temple_run()

        pygame.display.flip()
        CLOCK.tick(30)

        # Gestion de la fermeture du jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Lancement du jeu
main_room()
