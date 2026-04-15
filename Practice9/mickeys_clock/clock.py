import os
import math
import datetime
import pygame


class MickeyClock:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mickey's Clock")

        self.clock = pygame.time.Clock()
        self.running = True

        self.bg_color = (180, 180, 180)
        self.black = (0, 0, 0)

        self.center = pygame.Vector2(self.width // 2, self.height // 2)
        self.radius = 220

        self.font = pygame.font.SysFont("Arial", 36)

        base_path = os.path.dirname(__file__)
        hand_path = os.path.join(base_path, "images", "mickey_hand.png")

        self.hand_original = pygame.image.load(hand_path).convert_alpha()
        self.hand_original = pygame.transform.smoothscale(self.hand_original, (140, 140))

        # wrist point inside hand image
        # adjust a little if needed
        self.wrist_x = self.hand_original.get_width() // 2
        self.wrist_y = int(self.hand_original.get_height() * 0.82)

    def get_time(self):
        now = datetime.datetime.now()
        return now.minute, now.second

    def draw_clock_face(self):
        pygame.draw.circle(
            self.screen,
            self.black,
            (int(self.center.x), int(self.center.y)),
            self.radius,
            3
        )

        for i in range(60):
            angle = math.radians(i * 6 - 90)

            if i % 5 == 0:
                tick_len = 20
                tick_width = 3
            else:
                tick_len = 10
                tick_width = 1

            x1 = self.center.x + (self.radius - tick_len) * math.cos(angle)
            y1 = self.center.y + (self.radius - tick_len) * math.sin(angle)
            x2 = self.center.x + self.radius * math.cos(angle)
            y2 = self.center.y + self.radius * math.sin(angle)

            pygame.draw.line(self.screen, self.black, (x1, y1), (x2, y2), tick_width)

    def draw_digital_time(self, minute, second):
        text = f"{minute:02}:{second:02}"
        text_surface = self.font.render(text, True, self.black)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 + 150))
        self.screen.blit(text_surface, text_rect)

    def draw_hand(self, angle_degrees, width_scale, height_scale, mirror=False):
        new_width = int(self.hand_original.get_width() * width_scale)
        new_height = int(self.hand_original.get_height() * height_scale)

        image = pygame.transform.smoothscale(self.hand_original, (new_width, new_height))

        if mirror:
            image = pygame.transform.flip(image, True, False)

        w, h = image.get_size()

        wrist_x = w // 2
        wrist_y = int(h * 0.82)

        rotated_image = pygame.transform.rotate(image, -angle_degrees)
        rotated_rect = rotated_image.get_rect()

        center_to_wrist = pygame.Vector2(wrist_x - w / 2, wrist_y - h / 2)
        rotated_offset = center_to_wrist.rotate(angle_degrees)

        rotated_rect.center = self.center - rotated_offset

        self.screen.blit(rotated_image, rotated_rect)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.draw_clock_face()

        minute, second = self.get_time()

        minute_angle = minute * 6
        second_angle = second * 6

        # minute hand = shorter, a bit wider
        self.draw_hand(minute_angle, 0.85, 0.85)

        # second hand = thinner and longer, mirrored
        self.draw_hand(second_angle, 0.65, 1.20, mirror=True)

        pygame.draw.circle(
            self.screen,
            self.black,
            (int(self.center.x), int(self.center.y)),
            7
        )

        self.draw_digital_time(minute, second)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()