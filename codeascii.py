import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Système de sécurité")

VERT = (0, 255, 0)
NOIR = (0, 0, 0)

font = pygame.font.Font(None, 32)


def afficher_texte(texte, x, y):
  """affiche un texte à l'écran"""
  surface_texte = font.render(texte, True, VERT)
  screen.blit(surface_texte, (x, y))


def generer_code():
  """génère le code secret"""
  longueur = 12
  return [random.randint(65, 90) for _ in range(longueur)]


def main():
  """fonction principale du jeu"""
  code = generer_code()
  texte_entre = ""
  message = ""
  essais = 3
  debut = time.time()

  en_cours = True
  while en_cours:
    temps_ecoule = time.time() - debut
    if temps_ecoule >= 120:
      en_cours = False

    screen.fill(NOIR)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        en_cours = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          attendu = ''.join(chr(c) for c in code)
          if texte_entre == attendu:
            message = "CORRECT!"
            code = generer_code()
          else:
            essais -= 1
            message = "ERREUR!"
          texte_entre = ""
        elif event.key == pygame.K_BACKSPACE:
          texte_entre = texte_entre[:-1]
        elif len(texte_entre) < 5:
          texte_entre += event.unicode.upper()

    if essais <= 0:
      en_cours = False

    afficher_texte("Mot de passe requis pour ouvrir la porte:", 50, 50)
    afficher_texte(f"Temps: {int(120 - temps_ecoule)}s", 50, 100)
    afficher_texte(f"Essais: {essais}", 50, 150)

    txt_code = " ".join(str(c) for c in code)
    afficher_texte(f"Code ASCII: {txt_code}", 50, 200)

    afficher_texte(f"> {texte_entre}", 50, 300)
    afficher_texte(message, 50, 400)

    pygame.display.flip()

  pygame.quit()


if __name__ == "__main__":
  main()
