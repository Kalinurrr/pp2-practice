import os
import pygame
from player import MusicPlayer


class MusicPlayerApp:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Music Player")

        self.clock = pygame.time.Clock()
        self.running = True

        self.bg_color = (30, 30, 30)
        self.white = (255, 255, 255)
        self.gray = (180, 180, 180)
        self.green = (100, 220, 100)
        self.blue = (80, 160, 255)
        self.red = (220, 90, 90)

        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

        base_path = os.path.dirname(__file__)
        music_folder = os.path.join(base_path, "music")

        self.player = MusicPlayer(music_folder)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_progress_bar(self):
        bar_x = 100
        bar_y = 250
        bar_width = 600
        bar_height = 20

        pygame.draw.rect(self.screen, self.gray, (bar_x, bar_y, bar_width, bar_height), 2)

        if self.player.track_length > 0:
            progress = self.player.get_progress_seconds() / self.player.track_length
            progress = max(0, min(progress, 1))
            fill_width = int(bar_width * progress)
            pygame.draw.rect(self.screen, self.blue, (bar_x, bar_y, fill_width, bar_height))

    def draw_ui(self):
        self.screen.fill(self.bg_color)

        self.draw_text("Music Player", self.title_font, self.white, 280, 40)
        self.draw_text(f"Current Track: {self.player.get_current_track_name()}", self.text_font, self.green, 80, 120)

        if not self.player.playlist:
            status = "Status: No tracks found"
            color = self.red
        elif self.player.is_playing:
            status = "Status: Playing"
            color = self.green
        else:
            status = "Status: Stopped"
            color = self.red

        self.draw_text(status, self.text_font, color, 80, 170)

        self.draw_progress_bar()
        self.draw_text(self.player.get_progress_text(), self.small_font, self.white, 310, 285)

        self.draw_text("P = Play", self.small_font, self.white, 80, 340)
        self.draw_text("S = Stop", self.small_font, self.white, 80, 370)
        self.draw_text("N = Next", self.small_font, self.white, 80, 400)
        self.draw_text("B = Previous", self.small_font, self.white, 80, 430)
        self.draw_text("Q = Quit", self.small_font, self.white, 80, 460)

        pygame.display.flip()

    def handle_keydown(self, key):
        print("Pressed key:", key)

        if key == pygame.K_p:
            self.player.play()
        elif key == pygame.K_s:
            self.player.stop()
        elif key == pygame.K_n:
            self.player.next_track()
        elif key == pygame.K_b:
            self.player.previous_track()
        elif key == pygame.K_q:
            self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)

            self.player.update()
            self.draw_ui()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    app = MusicPlayerApp()
    app.run()