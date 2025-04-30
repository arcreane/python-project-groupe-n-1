import pygame
import sys
import random
import time

# Initialisation Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("L'équation mortelle")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (150, 150, 150)

# Police
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Background temporaire
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((50, 50, 100))

# Joueur temporaire
player_size = 50
player = pygame.Rect(100, HEIGHT // 2 - player_size // 2, player_size, player_size)  # Centré verticalement
player_speed = 5

# Coffre temporaire
chest_rect = pygame.Rect(600, HEIGHT // 2 - 30, 60, 60)

# Inconnues
unknowns = {}
answers = {}

def draw_room(show_message=False):
    SCREEN.blit(background, (0, 0))
    pygame.draw.rect(SCREEN, (160, 82, 45), chest_rect)
    pygame.draw.rect(SCREEN, GREEN, player)

    if show_message:
        text = small_font.render("Appuie sur A pour ouvrir le coffre", True, WHITE)
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

def main_room():
    clock = pygame.time.Clock()
    running = True
    near_chest = False

    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        # Empêche de sortir de l'écran
        player.clamp_ip(SCREEN.get_rect())

        near_chest = player.colliderect(chest_rect)

        draw_room(show_message=near_chest)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and near_chest:
                    equation()
                    running = False

def draw_all(equations, current_input, timer, solving_final=False):
    SCREEN.fill(BLACK)

    # Consigne
    instruction_text = small_font.render("Entrez chaque résultat pour trouver A, B et C.", True, GRAY)
    SCREEN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 10))

    y_pos = 70
    for idx, (text, solved) in enumerate(equations.items()):
        color = GREEN if solved else WHITE
        eq_text = font.render(text, True, color)
        SCREEN.blit(eq_text, (WIDTH // 2 - eq_text.get_width() // 2, y_pos))

        if solved and idx < 3:
            var_name = ['A', 'B', 'C'][idx]
            found_value = unknowns.get(var_name, None)
            if found_value is not None:
                result_text = small_font.render(f"{var_name} = {found_value}", True, GREEN)
                SCREEN.blit(result_text, (WIDTH // 2 + eq_text.get_width() // 2 + 20, y_pos + 10))

        y_pos += 70

    input_text = font.render(current_input, True, GREEN if current_input.isdigit() else RED)
    SCREEN.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, y_pos + 30))

    timer_text = font.render(f"Temps restant: {timer}s", True, WHITE)
    SCREEN.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT - 100))

    pygame.display.flip()

def equation():
    # Générer A, B et C
    A = random.randint(1, 9)
    B = random.randint(1, 9)
    C = random.randint(1, 9)

    equations_text = {
        f"2 + A = {2 + A}": False,
        f"3 × B + 7 = {3 * B + 7}": False,
        f"C + C + C = {3 * C}": False
    }
    solutions = [A, B, C]
    unknown_keys = ['A', 'B', 'C']

    final_equation_text = f"A + 2 × B + 3 × C = ?"
    final_solution = A + 2 * B + 3 * C

    all_equations = {**equations_text, final_equation_text: False}

    solving_final = False
    user_input = ""
    current_idx = 0

    time_limit = 60
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(time_limit - elapsed))

        draw_all(all_equations, user_input, time_left, solving_final)

        if time_left == 0:
            show_final_message("Temps écoulé. Game over !", RED)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_input.isdigit():
                    if not solving_final:
                        if int(user_input) == solutions[current_idx]:
                            key = list(equations_text.keys())[current_idx]
                            all_equations[key] = True
                            unknowns[unknown_keys[current_idx]] = int(user_input)
                            current_idx += 1
                            user_input = ""
                            if current_idx == 3:
                                solving_final = True
                        else:
                            show_final_message("Mauvaise réponse. Game over !", RED)
                            running = False
                    else:
                        if int(user_input) == final_solution:
                            all_equations[final_equation_text] = True
                            show_final_message("Bravo, Énigme Résolue!", GREEN)
                        else:
                            show_final_message("Mauvaise réponse. Game over !", RED)
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():
                    user_input += event.unicode

def show_final_message(message, color):
    SCREEN.fill(BLACK)
    text = font.render(message, True, color)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(3)


main_room()
