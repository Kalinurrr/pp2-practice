import pygame
from ball import Ball


class MovingBallGame:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Moving Ball Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.white = (255, 255, 255)

        self.ball = Ball(
            x=self.width // 2,
            y=self.height // 2,
            radius=25,
            color=(255, 0, 0),
            screen_width=self.width,
            screen_height=self.height,
            step=20
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.ball.move_up()
                elif event.key == pygame.K_DOWN:
                    self.ball.move_down()
                elif event.key == pygame.K_LEFT:
                    self.ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.ball.move_right()

    def draw(self):
        self.screen.fill(self.white)
        self.ball.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = MovingBallGame()
    game.run()