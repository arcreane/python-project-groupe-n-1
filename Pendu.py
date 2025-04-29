#Importations des différents modules
import pygame
import sys
import random
import time

pygame.init()

#Initialisation de la fenêtre
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h #S'adapte à la résolution de l'ordinateur
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-jeu : Le Pendu")

#Initialisation du fond
background_image = pygame.image.load("Images/background_zoom.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

#Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)

#Initialisation du texte
font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 80)

#Fonction pour définir les mots à trouver
def load_words():
    try:
        with open("dict.txt", "r", encoding="utf-8") as file:
            words = file.read().splitlines()
        return [word.strip().lower() for word in words if len(word) > 3]
    except Exception as e:
        print(f"Erreur de chargement du fichier : {e}")
        return ["Python", "Pendu", "Jeu", "Informatique", "Ordinateur", "Pycharm", "Binaire"]

word_list = load_words()

#Fonction pour afficher le texte
def show_message(message, color=GREEN, duration=3):
    SCREEN.blit(background_image, (0,0))
    text = font.render(message, True, color)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(duration)

#Fonction pour afficher les stats
def display_stats(stats):
    SCREEN.blit(background_image, (0, 0))  # Utilisation de background_image
    y = 400
    for key, value in stats.items():
        line = small_font.render(f"{key.replace('_', ' ').capitalize()} : {value}", True, WHITE)
        SCREEN.blit(line, (WIDTH // 2 - line.get_width() // 2, y))
        y += 80
    pygame.display.flip()
    time.sleep(3)

#Jeu principal
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
        SCREEN.blit(background_image, (0, 0))
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

        # Si le mot est trouvé
        if '_' not in guessed:
            show_message("Vous avez trouvé le mot !", GREEN, duration=4)
            import Salle2.py #Importation de la deuxième salle si le joueur réussit
            break

    #Si le joueur a échoué
    if attempts == 0:
        show_message("Vous avez perdu. Game Over.", RED, 3)
        pygame.quit()
        sys.exit()

pendu()
