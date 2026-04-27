import os
import random
import pygame

from persistence import save_score, DIFFICULTY

WIDTH = 600
HEIGHT = 800
FPS = 60

ROAD_LEFT = 120
ROAD_RIGHT = 480
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANES = 4
LANE_WIDTH = ROAD_WIDTH // LANES

WHITE = (245, 245, 245)
BLACK = (20, 20, 25)
ROAD = (55, 55, 60)
GRASS = (35, 120, 55)
YELLOW = (241, 196, 15)
RED = (231, 76, 60)
ORANGE = (230, 126, 34)
GREEN = (46, 204, 113)
CYAN = (26, 188, 156)

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def load_image(filename, size):
    path = os.path.join(ASSETS_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    return image


class Player:
    def __init__(self, image):
        self.w = 46
        self.h = 78
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 125
        self.speed = 7
        self.image = image
        self.active_power = None
        self.power_timer = 0
        self.shield = False

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(ROAD_LEFT + 5, min(self.x, ROAD_RIGHT - self.w - 5))
        self.y = max(80, min(self.y, HEIGHT - self.h - 10))

    def activate_power(self, power_name):
        if self.active_power is not None:
            return

        if power_name == "nitro":
            self.active_power = "nitro"
            self.power_timer = 4

        elif power_name == "shield":
            self.active_power = "shield"
            self.shield = True

    def update_power(self, dt):
        if self.active_power == "nitro":
            self.power_timer -= dt

            if self.power_timer <= 0:
                self.active_power = None
                self.power_timer = 0

    def use_shield(self):
        if self.shield:
            self.shield = False
            self.active_power = None
            return True

        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        if self.shield:
            pygame.draw.ellipse(screen, CYAN, self.rect.inflate(20, 20), 3)


class TrafficCar:
    def __init__(self, lane, y, speed, image):
        self.w = 46
        self.h = 78
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.w // 2
        self.y = y
        self.speed = speed
        self.image = image

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, speed_bonus):
        self.y += self.speed + speed_bonus

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Coin:
    def __init__(self, lane, y, image):
        self.size = 30
        self.value = random.choice([1, 2, 5])
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.size // 2
        self.y = y
        self.speed = 5
        self.image = image

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, speed_bonus):
        self.y += self.speed + speed_bonus

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, lane, y, kind):
        self.size = 44
        self.kind = kind
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.size // 2
        self.y = y
        self.speed = 5

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, speed_bonus):
        self.y += self.speed + speed_bonus

    def draw(self, screen):
        if self.kind == "barrier":
            pygame.draw.rect(screen, ORANGE, self.rect, border_radius=6)
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x + self.size, self.y + self.size), 5)
            pygame.draw.line(screen, BLACK, (self.x + self.size, self.y), (self.x, self.y + self.size), 5)

        elif self.kind == "oil":
            pygame.draw.ellipse(screen, BLACK, self.rect)
            pygame.draw.ellipse(screen, (70, 70, 75), self.rect.inflate(-14, -16))

        elif self.kind == "pothole":
            pygame.draw.circle(screen, (65, 65, 70), self.rect.center, self.size // 2)
            pygame.draw.circle(screen, BLACK, self.rect.center, self.size // 3)


class RoadEvent:
    def __init__(self, lane, y, kind):
        self.w = 64
        self.h = 30
        self.kind = kind
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.w // 2
        self.y = y
        self.speed = 5
        self.direction = random.choice([-1, 1])

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, speed_bonus):
        self.y += self.speed + speed_bonus

        if self.kind == "moving_barrier":
            self.x += self.direction * 2

            if self.x < ROAD_LEFT + 5 or self.x + self.w > ROAD_RIGHT - 5:
                self.direction *= -1

    def draw(self, screen):
        if self.kind == "speed_bump":
            pygame.draw.rect(screen, YELLOW, self.rect, border_radius=6)
            pygame.draw.line(screen, BLACK, (self.x + 5, self.y + 8), (self.x + self.w - 5, self.y + 8), 3)
            pygame.draw.line(screen, BLACK, (self.x + 5, self.y + 22), (self.x + self.w - 5, self.y + 22), 3)

        elif self.kind == "moving_barrier":
            pygame.draw.rect(screen, RED, self.rect, border_radius=6)

        elif self.kind == "nitro_strip":
            pygame.draw.rect(screen, CYAN, self.rect, border_radius=6)
            pygame.draw.polygon(screen, WHITE, [
                (self.x + 14, self.y + 5),
                (self.x + 40, self.y + self.h // 2),
                (self.x + 14, self.y + self.h - 5)
            ])


class PowerUp:
    def __init__(self, lane, y, kind, nitro_image):
        self.size = 34
        self.kind = kind
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.size // 2
        self.y = y
        self.speed = 5
        self.life = 7
        self.nitro_image = nitro_image

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, dt, speed_bonus):
        self.y += self.speed + speed_bonus
        self.life -= dt

    def draw(self, screen):
        if self.kind == "nitro":
            screen.blit(self.nitro_image, (self.x, self.y))

        elif self.kind == "shield":
            pygame.draw.circle(screen, CYAN, self.rect.center, self.size // 2)
            pygame.draw.circle(screen, WHITE, self.rect.center, self.size // 2, 2)

            font = pygame.font.SysFont("Verdana", 17, bold=True)
            text = font.render("S", True, BLACK)
            screen.blit(text, text.get_rect(center=self.rect.center))

        elif self.kind == "repair":
            pygame.draw.circle(screen, GREEN, self.rect.center, self.size // 2)
            pygame.draw.circle(screen, WHITE, self.rect.center, self.size // 2, 2)

            font = pygame.font.SysFont("Verdana", 17, bold=True)
            text = font.render("+", True, BLACK)
            screen.blit(text, text.get_rect(center=self.rect.center))


def get_safe_lane(player):
    player_center = player.x + player.w // 2
    player_lane = int((player_center - ROAD_LEFT) // LANE_WIDTH)

    lanes = [0, 1, 2, 3]
    safe_lanes = [lane for lane in lanes if lane != player_lane]

    return random.choice(safe_lanes)


def draw_road(screen, road_offset):
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5)

    for lane in range(1, LANES):
        x = ROAD_LEFT + lane * LANE_WIDTH

        for y in range(-80, HEIGHT, 90):
            pygame.draw.rect(screen, WHITE, (x - 3, y + road_offset, 6, 45), border_radius=4)


def draw_hud(screen, font, username, score, distance, coins, active_power, power_timer):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 74))

    screen.blit(font.render(f"Name: {username}", True, WHITE), (10, 8))
    screen.blit(font.render(f"Score: {int(score)}", True, WHITE), (10, 38))

    screen.blit(font.render(f"Coins: {coins}", True, YELLOW), (190, 8))
    screen.blit(font.render(f"Distance: {int(distance)}m", True, WHITE), (190, 38))

    if active_power == "nitro":
        power_text = f"Nitro: {power_timer:.1f}s"
    elif active_power == "shield":
        power_text = "Shield: active"
    else:
        power_text = "Power: none"

    screen.blit(font.render(power_text, True, CYAN), (390, 8))


def run_game(screen, clock, settings, username):
    player_image = load_image(f"player_car_{settings['car_color']}.png", (46, 78))
    enemy_image = load_image("enemy_car.png", (46, 78))
    coin_image = load_image("coin.png", (30, 30))
    nitro_image = load_image("nitro.png", (34, 34))

    font = pygame.font.SysFont("Verdana", 18)
    config = DIFFICULTY[settings["difficulty"]]

    player = Player(player_image)

    traffic = []
    obstacles = []
    coins = []
    powerups = []
    events = []

    distance = 0
    coin_count = 0
    score = 0
    road_offset = 0

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, distance, coin_count

        player.move()
        player.update_power(dt)

        progress = 1 + distance / 3500
        base_speed = config["speed"]
        nitro_bonus = 4 if player.active_power == "nitro" else 0
        speed_bonus = (progress - 1) * 2 + nitro_bonus

        distance += (base_speed + nitro_bonus) * dt * 20
        road_offset = (road_offset + int(base_speed + nitro_bonus)) % 90

        traffic_chance = config["traffic_chance"] * progress
        obstacle_chance = config["obstacle_chance"] * progress
        powerup_chance = config["powerup_chance"]
        event_chance = 0.003 * progress

        if len(traffic) < 5 and random.random() < traffic_chance:
            lane = random.randrange(LANES)
            traffic.append(TrafficCar(lane, -90, base_speed + random.uniform(1, 3), enemy_image))

        if len(obstacles) < 4 and random.random() < obstacle_chance:
            lane = random.randrange(LANES)
            kind = random.choice(["barrier", "oil", "pothole"])
            obstacles.append(Obstacle(lane, -60, kind))

        if len(coins) < 6 and random.random() < 0.020:
            lane = get_safe_lane(player)
            coins.append(Coin(lane, -40, coin_image))

        if len(powerups) < 2 and random.random() < powerup_chance:
            lane = get_safe_lane(player)
            kind = random.choice(["nitro", "shield", "repair"])
            powerups.append(PowerUp(lane, -45, kind, nitro_image))

        if len(events) < 2 and random.random() < event_chance:
            lane = random.randrange(LANES)
            kind = random.choice(["moving_barrier", "speed_bump", "nitro_strip"])
            events.append(RoadEvent(lane, -45, kind))

        for item in traffic:
            item.update(speed_bonus)

        for item in obstacles:
            item.update(speed_bonus)

        for item in coins:
            item.update(speed_bonus)

        for item in events:
            item.update(speed_bonus)

        for item in powerups:
            item.update(dt, speed_bonus)

        traffic = [item for item in traffic if item.y < HEIGHT + 100]
        obstacles = [item for item in obstacles if item.y < HEIGHT + 100]
        coins = [item for item in coins if item.y < HEIGHT + 100]
        events = [item for item in events if item.y < HEIGHT + 100]
        powerups = [item for item in powerups if item.y < HEIGHT + 100 and item.life > 0]

        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coin_count += coin.value
                score += coin.value * 100
                coins.remove(coin)

        for power in powerups[:]:
            if player.rect.colliderect(power.rect):
                if power.kind == "repair":
                    if obstacles:
                        obstacles.pop(0)
                    score += 150
                else:
                    player.activate_power(power.kind)
                    score += 100

                powerups.remove(power)

        for road_event in events[:]:
            if player.rect.colliderect(road_event.rect):
                if road_event.kind == "nitro_strip":
                    player.activate_power("nitro")
                    events.remove(road_event)

                elif road_event.kind == "speed_bump":
                    distance = max(0, distance - 40)
                    events.remove(road_event)

                elif road_event.kind == "moving_barrier":
                    if player.use_shield():
                        events.remove(road_event)
                    else:
                        save_score(username, score, distance, coin_count)
                        return "game_over", score, distance, coin_count

        for car in traffic[:]:
            if player.rect.colliderect(car.rect):
                if player.use_shield():
                    traffic.remove(car)
                else:
                    save_score(username, score, distance, coin_count)
                    return "game_over", score, distance, coin_count

        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                if obstacle.kind == "oil":
                    player.x += random.choice([-45, 45])
                    player.x = max(ROAD_LEFT + 5, min(player.x, ROAD_RIGHT - player.w - 5))
                    obstacles.remove(obstacle)

                elif player.use_shield():
                    obstacles.remove(obstacle)

                else:
                    save_score(username, score, distance, coin_count)
                    return "game_over", score, distance, coin_count

        score = int(coin_count * 100 + distance)

        draw_road(screen, road_offset)

        for coin in coins:
            coin.draw(screen)

        for power in powerups:
            power.draw(screen)

        for road_event in events:
            road_event.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)

        for car in traffic:
            car.draw(screen)

        player.draw(screen)

        draw_hud(
            screen,
            font,
            username,
            score,
            distance,
            coin_count,
            player.active_power,
            player.power_timer
        )

        pygame.display.flip()