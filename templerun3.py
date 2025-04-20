import pygame
import sys
import random

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temple Escape")
CLOCK = pygame.time.Clock()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)

# Joueur
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 100, 50, 50)
player_speed = 10

# Obstacles et pièces
obstacles = []
coins = []
obstacle_timer = 0
coin_timer = 0
obstacle_interval = 30
coin_interval = 50
score = 0

# Vitesse
obstacle_speed = 7
coin_speed = 5

# Police
font = pygame.font.SysFont(None, 48)

def draw_text(text, color, y):
    t = font.render(text, True, color)
    SCREEN.blit(t, (WIDTH // 2 - t.get_width() // 2, y))

def temple_run():
    global obstacle_timer, obstacles, coin_timer, coins, score
    global obstacle_speed, coin_speed, obstacle_interval, coin_interval

    obstacles = []
    coins = []
    obstacle_timer = 0
    coin_timer = 0
    score = 0
    obstacle_speed = 7
    coin_speed = 5
    obstacle_interval = 30
    coin_interval = 50
    running = True

    while running:
        SCREEN.fill(BLACK)

        # Déplacement joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
            player.x += player_speed

        # Génération d'obstacles
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            obstacle_timer = 0
            x_pos = random.randint(0, WIDTH - 50)
            obstacles.append(pygame.Rect(x_pos, -50, 50, 50))

        # Génération de pièces
        coin_timer += 1
        if coin_timer >= coin_interval:
            coin_timer = 0
            x_pos = random.randint(0, WIDTH - 30)
            coins.append(pygame.Rect(x_pos, -30, 30, 30))

        # Mise à jour des obstacles
        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.y > HEIGHT:
                obstacles.remove(obs)
            if player.colliderect(obs):
                draw_text("Game Over!", RED, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(2000)
                return False

        # Mise à jour des pièces
        for coin in coins[:]:
            coin.y += coin_speed
            if coin.y > HEIGHT:
                coins.remove(coin)
            if player.colliderect(coin):
                score += 1
                coins.remove(coin)

        # Difficulté progressive
        if score > 0 and score % 5 == 0:
            obstacle_speed = 7 + score // 5
            coin_speed = 5 + score // 6
            obstacle_interval = max(15, 30 - score)

        if score >= 20:
            draw_text("Victoire! Vous vous êtes échappé!", GREEN, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            return True

        # Dessin
        pygame.draw.rect(SCREEN, GREEN, player)
        for obs in obstacles:
            pygame.draw.rect(SCREEN, RED, obs)
        for coin in coins:
            pygame.draw.ellipse(SCREEN, YELLOW, coin)
        draw_text(f"Score: {score}/20", WHITE, 20)

        pygame.display.flip()
        CLOCK.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    return True

# Lancer le jeu
if __name__ == "__main__":
    temple_run()