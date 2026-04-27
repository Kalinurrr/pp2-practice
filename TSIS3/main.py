import pygame

from racer import run_game, WIDTH, HEIGHT
from persistence import load_settings, save_settings, load_leaderboard
from ui import Button, draw_text, ask_username

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")
clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 25)
GRAY = (140, 140, 150)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
RED = (231, 76, 60)
PURPLE = (155, 89, 182)
YELLOW = (241, 196, 15)

title_font = pygame.font.SysFont("Verdana", 42, bold=True)
font = pygame.font.SysFont("Verdana", 25)
small_font = pygame.font.SysFont("Verdana", 18)


def main_menu():
    play_button = Button(190, 250, 220, 55, "Play", font, GREEN)
    leaderboard_button = Button(190, 320, 220, 55, "Leaderboard", font, BLUE)
    settings_button = Button(190, 390, 220, 55, "Settings", font, PURPLE)
    quit_button = Button(190, 460, 220, 55, "Quit", font, RED)

    while True:
        screen.fill(BLACK)

        draw_text(screen, "TSIS 3 RACER", title_font, WHITE, center=(WIDTH // 2, 130))
        draw_text(screen, "Advanced Driving & Power-Ups", small_font, GRAY, center=(WIDTH // 2, 185))

        play_button.draw(screen)
        leaderboard_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_button.clicked(event):
                return "play"

            if leaderboard_button.clicked(event):
                return "leaderboard"

            if settings_button.clicked(event):
                return "settings"

            if quit_button.clicked(event):
                return "quit"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back_button = Button(200, 710, 200, 50, "Back", font, RED)

    while True:
        leaderboard = load_leaderboard()

        screen.fill(BLACK)
        draw_text(screen, "TOP 10 SCORES", title_font, WHITE, center=(WIDTH // 2, 75))

        draw_text(screen, "Rank   Name        Score      Distance", small_font, YELLOW, topleft=(70, 125))

        y = 165

        if not leaderboard:
            draw_text(screen, "No scores yet", font, GRAY, center=(WIDTH // 2, 300))
        else:
            for index, item in enumerate(leaderboard, start=1):
                line = f"{index:<5} {item['name']:<10} {item['score']:<10} {item['distance']}m"
                draw_text(screen, line, small_font, WHITE, topleft=(70, y))
                y += 42

        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back_button.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def settings_screen(settings):
    color_button = Button(160, 240, 280, 52, "", font, PURPLE)
    difficulty_button = Button(160, 340, 280, 52, "", font, GREEN)
    back_button = Button(200, 650, 200, 50, "Back", font, RED)

    color_names = ["red", "white", "black"]
    difficulty_names = ["easy", "normal", "hard"]

    while True:
        screen.fill(BLACK)

        draw_text(screen, "SETTINGS", title_font, WHITE, center=(WIDTH // 2, 90))
        draw_text(screen, "Click buttons to change", small_font, GRAY, center=(WIDTH // 2, 145))

        color_button.text = f"Car color: {settings['car_color']}"
        difficulty_button.text = f"Difficulty: {settings['difficulty']}"

        color_button.draw(screen)
        difficulty_button.draw(screen)
        back_button.draw(screen)

        pygame.draw.rect(screen, (70, 70, 80), (230, 420, 140, 70), border_radius=12)

        preview_color = {
            "red": RED,
            "white": WHITE,
            "black": (10, 10, 10)
        }[settings["car_color"]]

        pygame.draw.rect(screen, preview_color, (280, 435, 40, 45), border_radius=8)
        pygame.draw.rect(screen, WHITE, (280, 435, 40, 45), 2, border_radius=8)

        draw_text(screen, "No sound version", small_font, GRAY, center=(WIDTH // 2, 535))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if color_button.clicked(event):
                current = color_names.index(settings["car_color"])
                settings["car_color"] = color_names[(current + 1) % len(color_names)]
                save_settings(settings)

            if difficulty_button.clicked(event):
                current = difficulty_names.index(settings["difficulty"])
                settings["difficulty"] = difficulty_names[(current + 1) % len(difficulty_names)]
                save_settings(settings)

            if back_button.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(score, distance, coins):
    retry_button = Button(180, 450, 240, 55, "Retry", font, GREEN)
    menu_button = Button(180, 525, 240, 55, "Main Menu", font, BLUE)

    while True:
        screen.fill(BLACK)

        draw_text(screen, "GAME OVER", title_font, RED, center=(WIDTH // 2, 130))
        draw_text(screen, f"Score: {int(score)}", font, WHITE, center=(WIDTH // 2, 230))
        draw_text(screen, f"Distance: {int(distance)} m", font, WHITE, center=(WIDTH // 2, 280))
        draw_text(screen, f"Coins: {int(coins)}", font, YELLOW, center=(WIDTH // 2, 330))

        retry_button.draw(screen)
        menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_button.clicked(event):
                return "retry"

            if menu_button.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def main():
    settings = load_settings()

    while True:
        action = main_menu()

        if action == "quit":
            break

        elif action == "leaderboard":
            result = leaderboard_screen()

            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen(settings)

            if result == "quit":
                break

            settings = load_settings()

        elif action == "play":
            username = ask_username(screen, clock, WIDTH, HEIGHT)

            while True:
                result, score, distance, coins = run_game(screen, clock, settings, username)

                if result == "quit":
                    pygame.quit()
                    return

                next_action = game_over_screen(score, distance, coins)

                if next_action == "retry":
                    continue

                if next_action == "menu":
                    break

                if next_action == "quit":
                    pygame.quit()
                    return

    pygame.quit()


if __name__ == "__main__":
    main()