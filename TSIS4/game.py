import pygame
import random
import json
import os
import db


WIDTH = 800
HEIGHT = 600
CELL = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)
RED = (200, 0, 0)
DARK_RED = (120, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 220, 0)
PURPLE = (160, 0, 200)
GREEN = (0, 200, 0)

SETTINGS_FILE = "settings.json"


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen, font):
        pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=10)
        label = font.render(self.text, True, WHITE)
        screen.blit(
            label,
            (
                self.rect.centerx - label.get_width() // 2,
                self.rect.centery - label.get_height() // 2
            )
        )

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 26)
        self.big_font = pygame.font.SysFont("Arial", 48)

        self.settings = self.load_settings()

        self.eat_sound = self.load_sound("assets/eat.mp3")
        self.gameover_sound = self.load_sound("assets/gameover.mp3")

        self.username = ""
        self.personal_best = 0
        self.running = True

    def load_sound(self, path):
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None

    def play_sound(self, sound):
        if self.settings["sound"] and sound:
            sound.play()

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            data = {
                "snake_color": [0, 200, 0],
                "grid": True,
                "sound": True
            }
            with open(SETTINGS_FILE, "w") as file:
                json.dump(data, file, indent=4)
            return data

        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def draw_text(self, text, x, y, color=WHITE, font=None):
        if font is None:
            font = self.font
        label = font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WIDTH, y))

    def random_position(self, snake, obstacles):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            pos = (x, y)

            if pos not in snake and pos not in obstacles:
                return pos

    def spawn_obstacles(self, snake, level):
        obstacles = []

        if level < 3:
            return obstacles

        count = level + 3

        while len(obstacles) < count:
            pos = self.random_position(snake, obstacles)

            head = snake[0]
            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if distance > CELL * 3:
                obstacles.append(pos)

        return obstacles

    def username_screen(self):
        self.username = ""

        while True:
            self.screen.fill(BLACK)
            self.draw_text("Enter username:", 250, 180, WHITE, self.big_font)
            self.draw_text(self.username, 300, 260, YELLOW, self.big_font)
            self.draw_text("Press ENTER to continue", 250, 340, GRAY)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.username.strip():
                        self.personal_best = db.get_personal_best(self.username)
                        return

                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]

                    else:
                        if len(self.username) < 15:
                            self.username += event.unicode

    def main_menu(self):
        play_btn = Button("Play", 300, 180, 200, 50)
        leader_btn = Button("Leaderboard", 300, 250, 200, 50)
        settings_btn = Button("Settings", 300, 320, 200, 50)
        quit_btn = Button("Quit", 300, 390, 200, 50)

        while self.running:
            self.screen.fill(BLACK)

            self.draw_text("SNAKE GAME", 250, 80, GREEN, self.big_font)
            self.draw_text(f"Player: {self.username}", 20, 20, WHITE)
            self.draw_text(f"Personal Best: {self.personal_best}", 20, 50, YELLOW)

            for btn in [play_btn, leader_btn, settings_btn, quit_btn]:
                btn.draw(self.screen, self.font)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if play_btn.clicked(event):
                    self.play_game()

                if leader_btn.clicked(event):
                    self.leaderboard_screen()

                if settings_btn.clicked(event):
                    self.settings_screen()

                if quit_btn.clicked(event):
                    self.running = False

    def play_game(self):
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = (CELL, 0)
        next_direction = direction

        score = 0
        level = 1
        base_speed = 8
        speed = base_speed

        obstacles = []
        food = self.random_position(snake, obstacles)
        food_weight = random.choice([1, 2, 3])
        food_spawn_time = pygame.time.get_ticks()

        poison = self.random_position(snake, obstacles)

        power_up = None
        power_type = None
        power_spawn_time = 0

        speed_effect_end = 0
        shield = False

        game_active = True

        while game_active:
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, CELL):
                        next_direction = (0, -CELL)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                        next_direction = (0, CELL)
                    elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                        next_direction = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                        next_direction = (CELL, 0)

            direction = next_direction

            if now > speed_effect_end:
                speed = base_speed + level

            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            collision = (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake or
                new_head in obstacles
            )

            if collision:
                if shield:
                    shield = False
                    new_head = snake[0]
                else:
                    game_active = False
                    break

            snake.insert(0, new_head)

            if new_head == food:
                self.play_sound(self.eat_sound)
                score += food_weight

                food = self.random_position(snake, obstacles)
                food_weight = random.choice([1, 2, 3])
                food_spawn_time = now

                if score // 5 + 1 > level:
                    level += 1
                    base_speed += 1
                    obstacles = self.spawn_obstacles(snake, level)

            else:
                snake.pop()

            if now - food_spawn_time > 7000:
                food = self.random_position(snake, obstacles)
                food_weight = random.choice([1, 2, 3])
                food_spawn_time = now

            if new_head == poison:
                for _ in range(2):
                    if len(snake) > 0:
                        snake.pop()

                if len(snake) <= 1:
                    game_active = False
                    break

                poison = self.random_position(snake, obstacles)

            if power_up is None and random.randint(1, 100) == 1:
                power_up = self.random_position(snake, obstacles)
                power_type = random.choice(["speed", "slow", "shield"])
                power_spawn_time = now

            if power_up and now - power_spawn_time > 8000:
                power_up = None
                power_type = None

            if power_up and new_head == power_up:
                if power_type == "speed":
                    speed = base_speed + level + 5
                    speed_effect_end = now + 5000

                elif power_type == "slow":
                    speed = max(4, base_speed + level - 4)
                    speed_effect_end = now + 5000

                elif power_type == "shield":
                    shield = True

                power_up = None
                power_type = None

            self.screen.fill(BLACK)
            self.draw_grid()

            pygame.draw.rect(
                self.screen,
                RED,
                (food[0], food[1], CELL, CELL)
            )

            food_text = self.font.render(str(food_weight), True, WHITE)
            self.screen.blit(food_text, (food[0] + 5, food[1] - 3))

            pygame.draw.rect(
                self.screen,
                DARK_RED,
                (poison[0], poison[1], CELL, CELL)
            )

            for block in obstacles:
                pygame.draw.rect(
                    self.screen,
                    GRAY,
                    (block[0], block[1], CELL, CELL)
                )

            if power_up:
                color = BLUE
                if power_type == "slow":
                    color = PURPLE
                elif power_type == "shield":
                    color = YELLOW

                pygame.draw.rect(
                    self.screen,
                    color,
                    (power_up[0], power_up[1], CELL, CELL)
                )

            snake_color = tuple(self.settings["snake_color"])
            for part in snake:
                pygame.draw.rect(
                    self.screen,
                    snake_color,
                    (part[0], part[1], CELL, CELL)
                )

            self.draw_text(f"Score: {score}", 20, 20)
            self.draw_text(f"Level: {level}", 20, 50)
            self.draw_text(f"Best: {self.personal_best}", 20, 80)

            if shield:
                self.draw_text("Shield: ON", 620, 20, YELLOW)

            pygame.display.update()
            self.clock.tick(speed)

        self.play_sound(self.gameover_sound)
        db.save_game(self.username, score, level)

        if score > self.personal_best:
            self.personal_best = score

        self.game_over_screen(score, level)

    def game_over_screen(self, score, level):
        retry_btn = Button("Retry", 300, 300, 200, 50)
        menu_btn = Button("Main Menu", 300, 370, 200, 50)

        while self.running:
            self.screen.fill(BLACK)

            self.draw_text("GAME OVER", 260, 120, RED, self.big_font)
            self.draw_text(f"Final Score: {score}", 300, 200)
            self.draw_text(f"Level Reached: {level}", 300, 235)
            self.draw_text(f"Personal Best: {self.personal_best}", 300, 270)

            retry_btn.draw(self.screen, self.font)
            menu_btn.draw(self.screen, self.font)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if retry_btn.clicked(event):
                    self.play_game()
                    return

                if menu_btn.clicked(event):
                    return

    def leaderboard_screen(self):
        back_btn = Button("Back", 300, 520, 200, 50)

        while self.running:
            self.screen.fill(BLACK)
            self.draw_text("LEADERBOARD", 250, 40, YELLOW, self.big_font)

            try:
                leaders = db.get_leaderboard()
            except Exception:
                leaders = []

            self.draw_text("Rank   Username        Score   Level   Date", 80, 120, WHITE)

            y = 160
            for i, row in enumerate(leaders, start=1):
                username, score, level, date = row
                date_text = date.strftime("%Y-%m-%d")
                text = f"{i:<6} {username:<14} {score:<7} {level:<7} {date_text}"
                self.draw_text(text, 80, y, GRAY)
                y += 35

            back_btn.draw(self.screen, self.font)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if back_btn.clicked(event):
                    return

    def settings_screen(self):
        grid_btn = Button("Toggle Grid", 280, 180, 240, 50)
        sound_btn = Button("Toggle Sound", 280, 250, 240, 50)
        color_btn = Button("Change Color", 280, 320, 240, 50)
        save_btn = Button("Save & Back", 280, 430, 240, 50)

        colors = [
            [0, 200, 0],
            [0, 100, 255],
            [255, 220, 0],
            [160, 0, 200],
            [255, 100, 0]
        ]

        color_index = 0

        while self.running:
            self.screen.fill(BLACK)

            self.draw_text("SETTINGS", 290, 80, YELLOW, self.big_font)
            self.draw_text(f"Grid: {self.settings['grid']}", 270, 140)
            self.draw_text(f"Sound: {self.settings['sound']}", 270, 160)

            pygame.draw.rect(
                self.screen,
                tuple(self.settings["snake_color"]),
                (550, 330, 40, 40)
            )

            for btn in [grid_btn, sound_btn, color_btn, save_btn]:
                btn.draw(self.screen, self.font)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if grid_btn.clicked(event):
                    self.settings["grid"] = not self.settings["grid"]

                if sound_btn.clicked(event):
                    self.settings["sound"] = not self.settings["sound"]

                if color_btn.clicked(event):
                    color_index = (color_index + 1) % len(colors)
                    self.settings["snake_color"] = colors[color_index]

                if save_btn.clicked(event):
                    self.save_settings()
                    return

    def run(self):
        self.username_screen()
        if self.running:
            self.main_menu()

        pygame.quit()