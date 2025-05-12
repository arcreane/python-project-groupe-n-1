import pygame
import sys
import random
import time


pygame.init()

# Paramètres fenêtre
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-jeu : Le Pendu")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)


font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Charger les mots depuis dict.txt
def load_words():
    try:
        with open("dict.txt", "r", encoding="utf-8") as file:
            words = file.read().splitlines()
        return [word.strip().lower() for word in words if len(word) > 3]
    except Exception as e:
        print(f"Erreur de chargement du fichier : {e}")
        return ["python", "pendu", "jeu"]

word_list = load_words()

# Affichage de message temporaire
def show_message(message, color=GREEN, duration=3):
    SCREEN.fill(BLACK)
    text = font.render(message, True, color)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(duration)

# Stats du jeu
def display_stats(stats):
    SCREEN.fill(BLACK)
    y = 200
    for key, value in stats.items():
        line = small_font.render(f"{key.replace('_', ' ').capitalize()} : {value}", True, WHITE)
        SCREEN.blit(line, (WIDTH // 2 - line.get_width() // 2, y))
        y += 40
    pygame.display.flip()
    time.sleep(4)

# Jeu du pendu
def pendu():
    word = random.choice(word_list)
    guessed = [word[0]] + ['_' for _ in word[1:]]
    attempts = 8
    used_letters = set()

    game_stats = {
        "mot_a_trouver": word,
        "lettres_utilisees": [],
        "tentatives_restantes": attempts,
        "mot_trouve": False
    }

    while attempts > 0 and '_' in guessed:
        SCREEN.fill(BLACK)
        word_display = font.render(" ".join(guessed), True, WHITE)
        SCREEN.blit(word_display, (WIDTH // 2 - word_display.get_width() // 2, 200))

        attempts_text = font.render(f"Tentatives restantes : {attempts}", True, RED)
        SCREEN.blit(attempts_text, (WIDTH // 2 - attempts_text.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                letter = event.unicode.lower()
                if letter.isalpha() and len(letter) == 1 and letter not in used_letters:
                    if letter in word:
                        for i, l in enumerate(word):
                            if l == letter:
                                guessed[i] = letter
                    else:
                        attempts -= 1
                    used_letters.add(letter)
                    game_stats["lettres_utilisees"].append(letter)
                    game_stats["tentatives_restantes"] = attempts

    game_stats["mot_trouve"] = '_' not in guessed

    if game_stats["mot_trouve"]:
        show_message("Bravo ! Vous avez gagné !", GREEN)
    else:
        show_message(f"Perdu ! Le mot était : {word}", RED)

    display_stats(game_stats)

pendu()
pygame.quit()
sys.exit()
