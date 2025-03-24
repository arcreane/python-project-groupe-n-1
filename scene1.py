import pygame
import sys
from pygame.locals import *
pygame.init()

largeur = 1920
hauteur = 1080
window = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Escape Game")

background = pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\background.jpg")
background = pygame.transform.scale(background, (largeur, hauteur))

sprite_idle = pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_idle.png")
sprite_idle = pygame.transform.scale(sprite_idle, (400, 400))
sprite_rect = sprite_idle.get_rect()

sprite_animation = [
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk1.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk1.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk3.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk4.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk5.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk6.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk7.png"),
    pygame.image.load(r"C:\Users\Lola SANCHEZ\OneDrive - ISEP\Semestre 2\Informatique\Escape_Game\Image\sprite_walk8.png")
]

sprite_animation = [pygame.transform.scale(img, (400, 400)) for img in sprite_animation]

x, y = 300, 450
sprite_rect = sprite_idle.get_rect(topleft=(x, y))


white = (255, 255, 255)


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
    
    font = pygame.font.SysFont('dejavuserif', 40)
    minutes = temps_restant // 60000
    secondes = (temps_restant % 60000) // 1000
    temps_str = f"{minutes:02}:{secondes:02}"
    texte = font.render(temps_str, True, white)
    screen.blit(texte, (largeur - 120, 20))

clock = pygame.time.Clock()
temps_depart = 20 * 60 * 1000  
temps_initial = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.blit(background, (0, 0))
    
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