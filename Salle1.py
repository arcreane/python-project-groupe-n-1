#Importations des différents modules
import pygame
import sys
from pygame.locals import *

pygame.init()

#Initialisation de la fenêtre
infoObject = pygame.display.Info() #S'adapte à la résolution de l'ordinateur
largeur, hauteur = infoObject.current_w, infoObject.current_h
window = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Escape Game")

#Initialisation du fond
background = pygame.image.load("Images/bathroom_room1.png")
background = pygame.transform.scale(background, (largeur, hauteur))

#Inititalisation du sprite
sprite_idle = pygame.image.load("Images/sprite.png")
sprite_idle = pygame.transform.scale(sprite_idle, (400, 400))
sprite_rect = sprite_idle.get_rect(topleft=(200, 450))

#Initialisation du bouton
zone_image = pygame.image.load("Images/button.png")
zone_image = pygame.transform.scale(zone_image, (100, 100))
zone_rect = zone_image.get_rect(topleft=(650, 400))  # Position du bouton

#Couleurs
white = (255, 255, 255)
black = (0, 0, 0)

#Vitesse de déplacement du sprite
vitesse = 9

#Fonction pour déplacer le sprite avec les flèches du clavier
def deplacer_sprite(rect, touches, vitesse):
    if touches[K_LEFT]:
        rect.x -= vitesse
    if touches[K_RIGHT]:
        rect.x += vitesse
    if touches[K_UP]:
        rect.y -= vitesse
    if touches[K_DOWN]:
        rect.y += vitesse
    return rect

#Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if zone_rect.collidepoint(pygame.mouse.get_pos()):
                import Pendu.py #Si le bouton est cliquer, on importe le fichier avec le pendu

    #Affichage des éléments
    window.blit(background, (0, 0))
    window.blit(zone_image, zone_rect)

    font = pygame.font.SysFont(None, 20)
    message = font.render("CLIQUE AVEC TA SOURIS SUR LE BOUTON !", True, white)
    message_x = zone_rect.x + zone_rect.width // 2 - message.get_width() // 2
    message_y = zone_rect.y - 50
    window.blit(message, (message_x, message_y))

    touches = pygame.key.get_pressed()
    sprite_rect = deplacer_sprite(sprite_rect, touches, vitesse)
    window.blit(sprite_idle, sprite_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
