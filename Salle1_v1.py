import pygame
import sys
from pygame.locals import *
import subprocess

pygame.init()

largeur = 1920
hauteur = 1080
window = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Escape Game")

background = pygame.image.load("bathroom_room1.png")
background = pygame.transform.scale(background, (largeur, hauteur))

sprite_idle = pygame.image.load("Idle.png")
sprite_idle = pygame.transform.scale(sprite_idle, (400, 400))
sprite_rect = sprite_idle.get_rect()

sprite_animation = [
    pygame.image.load("Walk1.png"),
    pygame.image.load("Walk2.png"),
    pygame.image.load("Walk3.png"),
    pygame.image.load("Walk4.png"),
    pygame.image.load("Walk5.png"),
    pygame.image.load("Walk6.png"),
    pygame.image.load("Walk7.png"),
    pygame.image.load("Walk8.png"),
    pygame.image.load("Walk9.png"),
    pygame.image.load("Walk10.png")
]
sprite_animation = [pygame.transform.scale(img, (400, 400)) for img in sprite_animation]

x, y = 500, 450
sprite_rect = sprite_idle.get_rect(topleft=(x, y))

# Zone cliquable (ex. un bouton)
zone_image = pygame.image.load("button.png")
zone_image = pygame.transform.scale(zone_image, (100, 100))
zone_rect = zone_image.get_rect(topleft=(800,500))  # position du "bouton"

white = (255, 255, 255)
black = (0, 0, 0)
vitesse = 3
animation_speed = 100
dernier_changement = pygame.time.get_ticks()
index_sprite = 0
moving = False

def deplacer_sprite(rect, touches, vitesse):
    moving = False
    if touches[pygame.K_LEFT]:
        rect.x -= vitesse
        moving = True
    if touches[pygame.K_RIGHT]:
        rect.x += vitesse
        moving = True
    if touches[pygame.K_UP]:
        rect.y -= vitesse
        moving = True
    if touches[pygame.K_DOWN]:
        rect.y += vitesse
        moving = True
    return rect, moving

def afficher_minuteur(screen, temps_restant):
    font = pygame.font.SysFont(None, 90)
    minutes = temps_restant // 60000
    secondes = (temps_restant % 60000) // 1000
    temps_str = f"{minutes:02}:{secondes:02}"
    texte = font.render(temps_str, True, black)
    screen.blit(texte, (largeur - 180, 20))

clock = pygame.time.Clock()
temps_depart = 20 * 60 * 1000
temps_initial = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # clic gauche
            if zone_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                import Pendu.py

    window.blit(background, (0, 0))
    window.blit(zone_image, zone_rect)

    touches = pygame.key.get_pressed()
    sprite_rect, moving = deplacer_sprite(sprite_rect, touches, vitesse)

    maintenant = pygame.time.get_ticks()
    if moving:
        if maintenant - dernier_changement > animation_speed:
            index_sprite = (index_sprite + 1) % len(sprite_animation)
            dernier_changement = maintenant
        window.blit(sprite_animation[index_sprite], sprite_rect)
    else:
        index_sprite = 0
        window.blit(sprite_idle, sprite_rect)

    temps_ecoule = pygame.time.get_ticks() - temps_initial
    temps_restant = max(0, temps_depart - temps_ecoule)
    afficher_minuteur(window, temps_restant)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()