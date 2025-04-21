
import pygame
import sys
import random
import time


pygame.init()

# Paramètres fenêtre
WIDTH, HEIGHT = 1920, 1080
background = pygame.image.load("background_zoom.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-jeu : Le Pendu")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 80)

def load_words():
    try:
        with open("dict.txt", "r", encoding="utf-8") as file:
            words = file.read().splitlines()
        return [word.strip().lower() for word in words if len(word) > 3]
    except Exception as e:
        print(f"Erreur de chargement du fichier : {e}")
        return ["Python", "Pendu", "Jeu", "Informatique", "Ordinateur", "Pycharm", "Binaire"]

word_list = load_words()

def show_message(message, color=GREEN, duration=3):
    SCREEN.fill(background)
    text = font.render(message, True, color)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(duration)

# Stats du jeu
def display_stats(stats):
    SCREEN.blit(background,(0,0))
    y = 400
    for key, value in stats.items():
        line = small_font.render(f"{key.replace('_', ' ').capitalize()} : {value}", True, WHITE)
        SCREEN.blit(line, (WIDTH // 2 - line.get_width() // 2, y))
        y += 80
    pygame.display.flip()
    time.sleep(3)

# Jeu du pendu
def pendu():
    word = random.choice(word_list)
    guessed = [word[0]] + ['_' for _ in word[1:]]
    attempts = 8
    used_letters = set()

    game_stats = {
        "mot_à_trouver": word,
        "lettres_utilisées": [],
        "tentatives_restantes": attempts
    }

    while attempts > 0 and '_' in guessed:
        SCREEN.blit(background,(0,0))
        word_display = font.render(" ".join(guessed), True, WHITE)
        SCREEN.blit(word_display, (WIDTH // 2 - word_display.get_width() // 2, 550))

        attempts_text = font.render(f"Tentatives restantes : {attempts}", True, BLACK)
        SCREEN.blit(attempts_text, (WIDTH // 2 - attempts_text.get_width() // 2, 450))

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
                    game_stats["lettres_utilisées"].append(letter)
                    game_stats["tentatives_restantes"] = attempts

    display_stats(game_stats)

pendu()
pygame.quit()
sys.exit()
